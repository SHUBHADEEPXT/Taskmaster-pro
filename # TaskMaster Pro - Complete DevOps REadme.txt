# TaskMaster Pro - Complete DevOps Pipeline

> **Note:** The main [README.md](./README.md) is the primary source of up-to-date project information. This file provides additional details and legacy documentation. Please refer to the main README for the latest setup and instructions.

## 🏗️ Project Overview
TaskMaster Pro is a modern task management application showcasing a complete DevOps pipeline with local Kubernetes deployment, monitoring, and GitOps practices.

## 🏠 Project Structure
```
taskmaster-pro/
├── src/                    # Frontend source code
│   ├── server.js           # Node.js frontend server
│   ├── templates/          # HTML templates
│   │   ├── index.html
│   │   └── login.html
│   └── static/             # Static assets
│       ├── css/            # Stylesheets
│       │   ├── css.css
│       │   └── login.css
│       └── js/             # JavaScript files
│           └── app.js
├── backend/                # Backend API (Python)
│   ├── main.py             # Python backend application
│   ├── requirements.txt    # Backend dependencies
│   └── Dockerfile          # Backend container config
├── kubernetes/             # Helm chart & K8s manifests
│   └── taskmaster/
│       ├── charts/         # Helm subcharts (PostgreSQL, Redis)
│       ├── templates/      # K8s YAML templates
│       └── values.yaml     # Helm values
├── ci-cd/                  # Jenkins pipeline configs/scripts
├── monitoring/             # Prometheus & Grafana setup
├── infrastructure/         # Infrastructure as Code
│   └── terraform/          # Terraform configurations
├── docs/                   # Documentation
│   └── day1.md             # Progress tracking
├── Dockerfile              # Main application container
├── docker-compose.yml      # Local development orchestration
├── requirements.txt        # Root level dependencies
└── README.md
```

## 🚀 Getting Started

### Prerequisites
- Docker Desktop (with WSL2 integration)
- Python 3.8+
- Git
- Kind (for local Kubernetes)
- kubectl

### Quick Start - Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/taskmaster-pro.git
   cd taskmaster-pro
   ```

2. **Run with Docker Compose:**
   ```bash
   # Start all services (FastAPI backend + Express frontend + PostgreSQL + Redis)
   docker-compose up --build
   
   # Access the application
   # Frontend: http://localhost:3000 (Express server)
   # Backend API: http://localhost:8000 (FastAPI with auto docs)
   # API Documentation: http://localhost:8000/docs (Swagger UI)
   ```

3. **Development Setup (Alternative):**
   ```bash
   # Terminal 1: Start FastAPI backend
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   uvicorn main:app --reload --port 8000
   
   # Terminal 2: Start Express frontend
   cd src
   npm install  # if you have package.json
   node server.js
   ```

### Kubernetes Local Deployment

1. **Install Kind:**
   ```bash
   curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64
   chmod +x ./kind
   sudo mv ./kind /usr/local/bin/kind
   ```

2. **Create local cluster:**
   ```bash
   kind create cluster --name taskmaster-cluster
   ```

3. **Deploy the application:**
   ```bash
   # Build and load Docker image
   docker build -t taskmaster:local ./backend/
   kind load docker-image taskmaster:local --name taskmaster-cluster
   
   # Deploy to Kubernetes
   kubectl apply -f kubernetes/
   
   # Access the application
   kubectl port-forward svc/taskmaster-service 8080:80 -n taskmaster
   ```

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI (Python)
- **Authentication**: JWT with HTTPBearer
- **Database**: PostgreSQL
- **Caching**: Redis
- **Container**: Docker

### Frontend
- **Server**: Express.js (Node.js)
- **Templates**: HTML5 with modern CSS
- **JavaScript**: Vanilla JS with responsive design
- **Static Assets**: CSS and JS served via Express

### DevOps & Infrastructure
- **Containerization**: Docker & Docker Compose
- **Orchestration**: Kubernetes (Kind for local)
- **CI/CD**: Jenkins (see ci-cd/README.md for details)
- **Monitoring**: Prometheus + Grafana
- **GitOps**: ArgoCD (planned)
- **Database**: PostgreSQL
- **Caching**: Redis

## 📈 Monitoring & Observability

### Local Monitoring Setup
```bash
# Start monitoring stack
docker-compose -f monitoring/docker-compose.monitoring.yml up -d

# Access dashboards
# Grafana: http://localhost:3000 (admin/admin)
# Prometheus: http://localhost:9090
```

### Kubernetes Monitoring
```bash
# Install monitoring stack
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install monitoring prometheus-community/kube-prometheus-stack

# Access Grafana
kubectl port-forward svc/monitoring-grafana 3000:80
```

## 🔄 CI/CD Pipeline

The Jenkins pipeline includes:
- **Linting:** Code quality checks (flake8)
- **Testing:** Automated unit tests (pytest)
- **Build:** Docker image creation
- **Push:** Docker image to registry
- **Deploy:** Automated deployment to Kind cluster

See [ci-cd/README.md](./ci-cd/README.md) for pipeline details, troubleshooting, and Jenkinsfile reference.

## 🔒 Security Features

- Container security scanning with Trivy
- Dependency vulnerability checks
- Kubernetes security policies
- Resource limits and quotas
- Network policies (planned)

## 📊 Performance Monitoring

Key metrics tracked:
- **Application:** Response time, error rate, throughput
- **Infrastructure:** CPU, memory, disk usage
- **Kubernetes:** Pod health, resource utilization

## 🎯 Project Goals & Learning Outcomes

This project demonstrates:
- **Local Kubernetes development** with Kind
- **GitOps practices** with automated deployments
- **Monitoring and observability** setup
- **Security-first approach** in containerization
- **Cost-effective DevOps** without cloud dependencies

## 📝 Documentation

- [Main README](./README.md)
- [CI/CD Details](./ci-cd/README.md)
- [Day-by-Day Progress](docs/progress.md)
- [Architecture Overview](docs/architecture.md)
- [Local Development Guide](docs/development.md)
- [Kubernetes Deployment](docs/kubernetes.md)
- [Monitoring Setup](docs/monitoring.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 🎉 Demo & Portfolio

**Live Demo Features:**
- ✅ Working todo application with CRUD operations
- ✅ Containerized with Docker
- ✅ Deployed on local Kubernetes cluster
- ✅ Monitoring with Prometheus & Grafana
- ✅ Automated CI/CD pipeline (Jenkins)
- ✅ GitOps workflow demonstration

**Portfolio Highlights:**
- Complete end-to-end DevOps pipeline