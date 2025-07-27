# CI/CD Pipeline - TaskMaster Pro

## Overview
This folder contains all configuration and documentation for the Jenkins-based CI/CD pipeline powering TaskMaster Pro.

---

## Pipeline Features
- **Automated Linting:** Python code checked with flake8
- **Automated Testing:** Backend tested with pytest
- **Docker Build & Push:** Backend and frontend images built and pushed to Docker Hub
- **Kubernetes Deploy:** Helm used to deploy both backend and frontend to the cluster
- **Quality Gates:** Pipeline fails on lint/test errors

---

## How It Works
- **Jenkinsfile** defines the pipeline stages (see root of repo)
- **Docker agent** ensures clean, reproducible builds
- **Pipeline triggers:**
  - On code push (webhook from GitHub)
  - On Pull Request (if configured)
  - Manual run from Jenkins UI
- **Artifacts:** Docker images tagged and pushed to Docker Hub
- **Deployment:** Helm upgrades backend and frontend in the cluster

---

## How to Trigger the Pipeline
- **Manual:** Click "Build Now" in Jenkins UI
- **Webhook:** Set up a webhook in your GitHub repo to POST to Jenkins on push
- **PR:** (Optional) Configure Jenkins to build on PR events

---

## Demo Instructions
- Show Jenkins UI with pipeline history
- Trigger a build (manual or via code push)
- Show each stage (Lint, Test, Build, Push, Deploy)
- Show successful deployment in Kubernetes (pods running)
- Reference screenshots in `docs/screenshots/`

---

## Troubleshooting
- **Docker permission errors:** Ensure Jenkins user is in the `docker` group and Docker socket is mounted
- **Python venv/PEP 668 errors:** Use a virtual environment for pip installs
- **Slow builds:** Allocate more CPU/RAM to Docker Desktop if needed
- **Image pull errors:** Check Docker Hub credentials and image tags
- **K8s deploy errors:** Check Helm values and pod logs

---

## References
- [Jenkinsfile](../Jenkinsfile)
- [README.md](../README.md)
- [docs/day6.md](../docs/day6.md)

---

> For more details, see daily logs and troubleshooting in `docs/`. 