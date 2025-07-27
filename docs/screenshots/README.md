# Screenshots for TaskMaster Pro Demo

This folder contains all screenshots required for portfolio, documentation, and demo purposes.

---

## Required Screenshots

### 1. Kubernetes
- Pods running (backend, frontend, PostgreSQL, Redis)
- Helm releases (helm list)

### 2. Application
- Frontend UI (http://localhost:3001)
- API docs (http://localhost:9000/api/docs)
- Health endpoint (http://localhost:9000/health)
- Prometheus metrics (http://localhost:9000/metrics)

### 3. Monitoring
- Prometheus UI (http://localhost:9090 if port-forwarded)
- Grafana dashboard (http://localhost:3000)
- ServiceMonitor YAML (kubernetes/taskmaster/templates/servicemonitor.yaml)

### 4. CI/CD
- Jenkins pipeline (all stages green)
- Jenkins build history
- Jenkins job configuration

### 5. Troubleshooting
- Any error messages and their fixes (optional, for challenges.md)

---

> For a full demo, walk through these screenshots in order, or show the live UI as described in the main README. 