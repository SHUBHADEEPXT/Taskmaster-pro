# CI/CD Documentation - TaskMaster Pro

This folder is dedicated to documenting all aspects of the CI/CD process for the TaskMaster Pro project.

## Jenkins Pipeline Overview

The current CI/CD pipeline is implemented using **Jenkins** and automates the following stages:

- **Lint:** Runs flake8 for Python code quality.
- **Test:** Runs backend tests (pytest).
- **Build:** Builds Docker image for backend.
- **Push:** Pushes Docker image to container registry.
- **Deploy:** Deploys to Kubernetes (via Helm or kubectl).

The pipeline uses a Docker agent for isolation and reproducibility. See the [Jenkinsfile](../Jenkinsfile) for the full pipeline script.

## Key Design Decisions
- **Jenkins** was chosen for its flexibility and local control.
- **Docker agent** ensures a clean, consistent environment for each stage.
- **Quality gates**: Linting and testing are required before build/push/deploy.

## Troubleshooting & Common Issues

- **Docker permission errors:**
  - Ensure the Jenkins user is in the `docker` group inside the Jenkins container.
  - Mount the Docker socket (`/var/run/docker.sock`) into the Jenkins container.
  - Restart Jenkins after changing group membership.
- **Python environment (PEP 668 error):**
  - Use a Python virtual environment in the Jenkins pipeline to avoid the externally-managed-environment error.
- **Slow pipeline:**
  - Increase Docker Desktop CPU/RAM allocation if running locally.
- **Jenkins data loss:**
  - Use a host path volume for Jenkins data persistence.

## Current Status
- Jenkins-based CI pipeline is set up for backend linting (flake8), testing (pytest), Docker build/push, and deployment.
- All linting errors have been fixed and the pipeline is green.
- Docker permission and Python environment issues have been resolved.
- Next steps: Add frontend tests and SonarQube integration (future).

## Suggestions for This Folder
- Add a `troubleshooting.md` for common CI/CD issues (see above for initial content).
- Add a `pipelines/` subfolder for different pipeline scripts (Jenkins, GitHub Actions, etc.).
- Document environment setup for Jenkins agents and runners.
- Keep this folder updated as you iterate on your CI/CD process. 