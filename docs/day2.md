#Day2
============

**Goals**
- Confirm Docker Desktop + WSL 2 works.
- Build multi-stage backend image.
- Bring up full dev stack (`docker compose up`).
- Spin up kind cluster, load image, deploy Nginx test.

**Key commands**
```bash
# Build image
docker build -t taskmaster-pro-backend:latest ./backend

# Dev stack
docker compose up -d

# kind cluster
kind create cluster --name dev
kind load docker-image taskmaster-pro-backend:latest --name dev

# Quick Nginx check
kubectl create deploy web --image=nginx:1.27
kubectl expose deploy web --port 80 --type NodePort
kubectl port-forward svc/web 8080:80  # → http://localhost:8080

