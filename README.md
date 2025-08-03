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
│   ├── taskmaster/       # Backend, DB, Redis
│   └── taskmaster-frontend/ # Frontend Helm chart
├── ci-cd/                # Jenkins pipeline configs/scripts
├── monitoring/           # Prometheus, Grafana setup
├── docs/                 # Daily docs & screenshots
│   ├── day1.md ... day6.md
│   └── screenshots/
└── README.md
```

---

## 🛤️ Day-by-Day Progress & Documentation
- 📖 **Daily logs:** See `docs/day1.md` ... `docs/day6.md` for step-by-step progress, learnings, and DevOps best practices.
- 🖼️ **Screenshots:** Visual progress in `docs/screenshots/` (cluster setup, health checks, dashboards, etc.).

---

## 🛠️ Tech Stack & Tools
- **Backend:** FastAPI (Python)
- **Frontend:** Node.js, HTML, CSS, JS (Dockerized)
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
- Backend Helm chart: `kubernetes/taskmaster/`
- Frontend Helm chart: `kubernetes/taskmaster-frontend/`
- Deploy backend:
  ```bash
  helm install taskmaster ./kubernetes/taskmaster -n taskmaster --create-namespace
  ```
- Deploy frontend:
  ```bash
  helm install taskmaster-frontend ./kubernetes/taskmaster-frontend -n taskmaster
  ```
- Port-forward backend API:
  ```bash
  kubectl port-forward -n taskmaster svc/taskmaster 9000:8000
  # Access API at http://localhost:9000
  ```
- Port-forward frontend:
  ```bash
  kubectl port-forward -n taskmaster svc/taskmaster-frontend 3001:3000
  # Access UI at http://localhost:3001
  ```

---

## 🖥️ Demo Instructions
1. **Start all port-forwards as above.**
2. **Visit:**
   - Frontend UI: [http://localhost:3001](http://localhost:3001)
   - API Docs: [http://localhost:9000/api/docs](http://localhost:9000/api/docs)
   - Health Endpoint: [http://localhost:9000/health](http://localhost:9000/health)
   - Prometheus Metrics: [http://localhost:9000/metrics](http://localhost:9000/metrics)
   - Grafana: [http://localhost:3000](http://localhost:3000) (login with admin/prom-operator)
3. **Show:**
   - Creating, updating, and deleting tasks in the UI
   - API endpoints in Swagger UI
   - Health and metrics endpoints
   - Live traffic and metrics in Prometheus/Grafana
   - Jenkins pipeline (see `ci-cd/README.md`)
4. **Screenshots:**
   - See `docs/screenshots/README.md` for a list of demo screenshots

---

## 🌐 How to Host Publicly
- **Cloud Hosting:**
  - Use a managed Kubernetes service (GKE, EKS, AKS, DigitalOcean, etc.)
  - Push images to Docker Hub or a private registry
  - Set up Ingress + DNS for your domain
  - Use a cloud database/cache or deploy PostgreSQL/Redis in-cluster
- **Domain:**
  - Buy a domain from a registrar (Namecheap, GoDaddy, etc.)
  - Point DNS to your cloud ingress controller
- **Limitations of Local Hosting:**
  - Local port-forwarding only works while your PC is running
  - For public access, use a cloud provider or tunneling service (ngrok, Cloudflare Tunnel)

---

## 📊 Monitoring
- Prometheus & Grafana manifests in `monitoring/`.
- See `docs/day4.md`, `docs/day6.md`, and screenshots for dashboards and setup.

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
- **Triggering:**
  - Pipeline can be triggered by code push (webhook), manual run, or PR.
  - See `ci-cd/README.md` for more details and troubleshooting steps.

---

## 🚦 Current Status
- **Full stack (frontend, backend, DB, cache) running in Kubernetes**
- **Monitoring and metrics available**
- **CI/CD pipeline green**
- **Screenshots and documentation up to date**
- **Ready for demo and portfolio**

---

## 🛣️ Future Roadmap
- Add ArgoCD for GitOps-style deployment
- Integrate GitHub Actions for cloud-native CI/CD
- Add advanced monitoring/alerting (Alertmanager, custom dashboards)
- Set up public cloud hosting and domain
- Implement best practices (RBAC, secrets management, autoscaling)
- Add more tests and code quality gates
- Document interview Q&A and demo scripts

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

---

> **Checkpoint:** See `docs/day6.md` for the latest milestone and demo instructions.
