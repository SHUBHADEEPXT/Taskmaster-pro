# main.py - FastAPI Backend for TaskMaster Pro
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import jwt
import hashlib
import os
from datetime import datetime, timedelta
import redis
import logging
from sqlalchemy import (
    create_engine, Column, Integer, String, Boolean, DateTime, Text
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import uvicorn
from starlette_exporter import PrometheusMiddleware, handle_metrics

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:password@localhost/taskmaster"
)
REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://localhost:6379"
)
JWT_SECRET = os.getenv(
    "JWT_SECRET",
    "your-super-secret-jwt-key-change-in-production"
)

logger.info("Starting TaskMaster Pro API...")
logger.info(f"Database URL: {DATABASE_URL}")
logger.info(f"Redis URL: {REDIS_URL}")

# Database setup
try:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    logger.info("Database connection established")
except Exception as e:
    logger.error(f"Database connection failed: {e}")
    raise

# Redis setup
try:
    redis_client = redis.from_url(REDIS_URL)
    redis_client.ping()  # Test connection
    logger.info("Redis connection established")
except Exception as e:
    redis_client = None
    logger.warning(f"Redis not available - caching disabled: {e}")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    completed = Column(Boolean, default=False)
    priority = Column(String, default="medium")
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    user_id = Column(Integer, index=True)
    tags = Column(String, nullable=True)  # JSON string of tags


try:
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")
except Exception as e:
    logger.error(f"Failed to create database tables: {e}")
    raise


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    email: str


class UserLogin(BaseModel):
    username: str
    password: str


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    priority: str = Field(
        default="medium",
        pattern="^(low|medium|high)$"
    )
    due_date: Optional[datetime] = None
    tags: Optional[List[str]] = []


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None
    tags: Optional[List[str]] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    priority: str
    due_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    tags: List[str]

    class Config:
        from_attributes = True


app = FastAPI(
    title="TaskMaster Pro API",
    description=(
        "Powerful task management API with  authentication & monitoring"
    ),    
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

app.add_middleware(
    PrometheusMiddleware,
    app_name="taskmaster-api",
    prefix="taskmaster_api",
    group_status_codes=True,
    group_urls=True
)
app.add_route("/metrics", handle_metrics)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, hashed_password: str) -> bool:
    return hash_password(password) == hashed_password


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        JWT_SECRET,
        algorithm="HS256"
    )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(
            credentials.credentials,
            JWT_SECRET,
            algorithms=["HS256"]
        )
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user


@app.get("/health")
async def health_check():
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "services": {
            "database": "unknown",
            "redis": "unknown"
        }
    }

    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        health_status["services"]["database"] = "healthy"
        db.close()
    except Exception as e:
        health_status["services"]["database"] = f"unhealthy: {str(e)}"
        health_status["status"] = "degraded"

    if redis_client:
        try:
            redis_client.ping()
            health_status["services"]["redis"] = "healthy"
        except Exception as e:
            health_status["services"]["redis"] = f"unhealthy: {str(e)}"
    else:
        health_status["services"]["redis"] = "disabled"

    return health_status


@app.post("/api/auth/register")
async def register(
    user: UserCreate, 
    db: Session = Depends(get_db)
    ):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")

    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)
    db_user = User(
        username=user.username,
        hashed_password=hashed_password,
        email=user.email
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    access_token = create_access_token(data={"sub": user.username})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {"username": user.username, "email": user.email}
    }


@app.post("/api/auth/login")
async def login(
    user: UserLogin, 
    db: Session = Depends(get_db)
    ):
    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.username})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {"username": user.username, "email": db_user.email}
    }


@app.get("/api/tasks", response_model=List[TaskResponse])
async def get_tasks(
    completed: Optional[bool] = None,
    priority: Optional[str] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Task).filter(Task.user_id == current_user.id)

    if completed is not None:
        query = query.filter(Task.completed == completed)

    if priority:
        query = query.filter(Task.priority == priority)

    if search:
        query = query.filter(Task.title.contains(search))

    tasks = query.order_by(Task.created_at.desc()).all()

    task_responses = []
    for task in tasks:
        task_dict = {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "priority": task.priority,
            "due_date": task.due_date,
            "created_at": task.created_at,
            "updated_at": task.updated_at,
            "tags": task.tags.split(",") if task.tags else []
        }
        task_responses.append(TaskResponse(**task_dict))

    return task_responses


@app.post("/api/tasks", response_model=TaskResponse)
async def create_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_task = Task(
        title=task.title,
        description=task.description,
        priority=task.priority,
        due_date=task.due_date,
        user_id=current_user.id,
        tags=",".join(task.tags) if task.tags else None
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    if redis_client:
        redis_client.delete(f"user_tasks_{current_user.id}")

    return TaskResponse(
        id=db_task.id,
        title=db_task.title,
        description=db_task.description,
        completed=db_task.completed,
        priority=db_task.priority,
        due_date=db_task.due_date,
        created_at=db_task.created_at,
        updated_at=db_task.updated_at,
        tags=db_task.tags.split(",") if db_task.tags else []
    )


@app.put("/api/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()

    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    for field, value in task_update.dict(exclude_unset=True).items():
        if field == "tags" and value is not None:
            setattr(db_task, field, ",".join(value))
        else:
            setattr(db_task, field, value)

    db_task.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_task)

    return TaskResponse(
        id=db_task.id,
        title=db_task.title,
        description=db_task.description,
        completed=db_task.completed,
        priority=db_task.priority,
        due_date=db_task.due_date,
        created_at=db_task.created_at,
        updated_at=db_task.updated_at,
        tags=db_task.tags.split(",") if db_task.tags else []
    )


@app.delete("/api/tasks/{task_id}")
async def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()

    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(db_task)
    db.commit()

    return {"message": "Task deleted successfully"}


@app.get("/api/stats")
async def get_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    total_tasks = db.query(Task).filter(Task.user_id == current_user.id).count()
    completed_tasks = db.query(Task).filter(
        Task.user_id == current_user.id,
        Task.completed.is_(True)
    ).count()

    overdue_tasks = db.query(Task).filter(
        Task.user_id == current_user.id,
        Task.completed.is_(False),
        Task.due_date < datetime.utcnow()
    ).count()

    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": total_tasks - completed_tasks,
        "overdue_tasks": overdue_tasks
    }


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )
