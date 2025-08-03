# Challenges & Troubleshooting Log

This document tracks major challenges faced and solutions found during the TaskMaster Pro DevOps project.

---

## Day 1: Project Setup & Git
- **Issue:** Git authentication failed (password removed by GitHub)
  - **Solution:** Used a Personal Access Token (PAT) for GitHub authentication.
- **Issue:** Frontend static files (CSS/JS) not loading
  - **Solution:** Fixed static file paths in HTML for both local and Docker environments.

## Day 2: Docker & Compose
- **Issue:** Docker Compose network issues
  - **Solution:** Ensured correct service names and ports in docker-compose.yml.

## Day 3: Kubernetes & Helm Bootstrap
- **Issue:** Pod CrashLoopBackOff due to missing DB
  - **Solution:** Switched to SQLite fallback for initial deployment.
- **Issue:** Helm values not picked up
  - **Solution:** Used correct env: block in values.yaml.

## Day 4: Database & Monitoring
- **Issue:** PostgreSQL/Redis not accessible in cluster
  - **Solution:** Fixed service names and namespaces in values.yaml.
- **Issue:** Prometheus/Grafana pods stuck in Pending
  - **Solution:** Waited for image pulls and checked node resources.

## Day 5: CI/CD Pipeline (Jenkins)
- **Issue:** Jenkins Docker permission errors
  - **Solution:** Added Jenkins user to docker group and matched group IDs.
- **Issue:** Python venv/PEP 668 errors
  - **Solution:** Used virtual environments in Jenkins pipeline.

## Day 6: Frontend Deployment & Full Stack
- **Issue:** Frontend not accessible after deploy
  - **Solution:** Set correct container/service ports and used port-forwarding on 3001.
- **Issue:** Metrics/health checks not working
  - **Solution:** Fixed SQLAlchemy health check with text() and ensured Prometheus endpoint exposed.

---

> More challenges and solutions can be added as the project evolves. If you faced a unique issue, add it here for future reference! 