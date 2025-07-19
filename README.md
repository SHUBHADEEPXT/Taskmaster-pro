# TaskMaster Pro - Complete DevOps Pipeline 🚀

## 🏗️ Project Overview
TaskMaster Pro is a modern, production-grade To-Do application built to showcase real-world DevOps skills. This project demonstrates a full DevOps pipeline, infrastructure-as-code, containerization, Kubernetes, monitoring, and more—perfect for your portfolio!

---

## 🏠 Project Structure
```
taskmaster-pro/
├── src/                  # Frontend (Node.js, HTML, CSS, JS)
│   ├── static/           # Static assets (css, js)
│   └── templates/        # HTML templates
├── backend/              # FastAPI backend (Python)
├── infrastructure/       # Terraform configs (infra-as-code)
├── kubernetes/           # Helm chart & K8s manifests
│   └── taskmaster/
│       ├── charts/       # Helm subcharts (PostgreSQL, Redis)
│       ├── templates/    # K8s YAML templates
│       └── values.yaml   # Helm values
├── ci-cd/                # Jenkins pipeline configs/scripts
├── monitoring/           # Prometheus, Grafana setup
├── docs/                 # Daily docs & screenshots
│   ├── day1.md
│   ├── day2.md
│   ├── day3.md
│   ├── day4.md
│   └── screenshots/
└── README.md
```

---

## 🛤️ Day-by-Day Progress & Documentation
- 📖 **Daily logs:** See `docs/day1.md`, `docs/day2.md`, `docs/day3.md`, `docs/day4.md` for step-by-step progress, learnings, and DevOps best practices.
- 🖼️ **Screenshots:** Visual progress in `docs/screenshots/` (cluster setup, health checks, dashboards, etc.).

---

## 🛠️ Tech Stack & Tools
- **Backend:** FastAPI (Python)
- **Frontend:** Node.js, HTML, CSS, JS
- **Database:** PostgreSQL (Helm subchart)
- **Cache:** Redis (Helm subchart)
- **Containerization:** Docker, Docker Compose
- **Orchestration:** Kubernetes (kind), Helm
- **Infrastructure:** Terraform
- **Monitoring:** Prometheus, Grafana
- **CI/CD:** Jenkins (see `ci-cd/` for pipeline scripts)

---

## 🚀 Getting Started

### Prerequisites
- Docker & Docker Compose
- Python 3.8+
- Node.js 14+
- Git
- WSL2 (recommended for Windows)
- kind (Kubernetes in Docker)
- Helm

### Local Development
1. **Clone the repo:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/taskmaster-pro.git
   cd taskmaster-pro
   ```
2. **Backend setup:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```
3. **Frontend setup:**
   ```bash
   cd ../src
   # (If needed: npm install)
   node server.js
   ```
4. **Run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

---

## ⚙️ Kubernetes & Helm
- Helm chart in `kubernetes/taskmaster/` manages backend, PostgreSQL, and Redis.
- Deploy with:
  ```bash
  helm install taskmaster ./kubernetes/taskmaster
  ```
- Customize via `values.yaml`.

---

## 📊 Monitoring
- Prometheus & Grafana manifests in `monitoring/`.
- See `docs/day4.md` and screenshots for dashboards and setup.

---

## 🔄 CI/CD Pipeline (Jenkins)
- Jenkins-based CI/CD pipeline automates linting, testing, Docker build/push, and deployment.
- Pipeline uses Docker agent for isolation and reproducibility.
- Key stages:
  - **Lint:** Runs flake8 for Python code quality.
  - **Test:** Runs backend tests (pytest).
  - **Build:** Builds Docker image for backend.
  - **Push:** Pushes Docker image to registry.
  - **Deploy:** Deploys to Kubernetes (via Helm or kubectl).
- **Troubleshooting:**
  - Docker permission errors: Ensure Jenkins user is in the `docker` group and Docker socket is mounted.
  - Python environment: Use virtual environments to avoid PEP 668 errors.
  - See `ci-cd/README.md` for more details and troubleshooting steps.

---

## 🤝 Contributing
1. Fork the repo
2. Create a feature branch
3. Commit your changes
4. Push and open a Pull Request

---

## 📝 License
MIT License. See [LICENSE](LICENSE).

---

> **Follow the journey:** Check daily docs and screenshots in `docs/` for a transparent, real-world DevOps build process!
