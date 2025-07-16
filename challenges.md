# Challenges Faced - TaskMaster Pro (Days 4 & 5)

## Day 4: Jenkins Setup & Initial CI
- **Jenkins Setup in Docker:**
  - Jenkins was started in a Docker container, but the default agent lacked Python and pip, causing initial pipeline failures.
  - Required entering the Jenkins container as root to install Python, pip, and system packages.
- **PEP 668 Error:**
  - Encountered the "externally-managed-environment" error when trying to use pip inside the Jenkins container.
  - Solution: Used a Python virtual environment for dependency installation in the Jenkins pipeline.
- **Jenkins Slowness:**
  - Jenkins UI and builds were slow due to low Docker Desktop resource allocation (CPU/RAM).
  - Solution: Increased Docker Desktop resources and stopped unused containers.
- **Jenkinsfile & Pipeline Issues:**
  - Multiple iterations to get the Jenkinsfile working with the right agent, Python, and flake8 setup.
  - Had to exclude the venv directory from flake8 to avoid performance issues.

## Day 5: Linting, Flake8, and CI Quality Gates
- **Flake8 Linting Errors:**
  - Many style/code issues (E501, F401, W293, etc.) in backend/main.py caused pipeline failures.
  - Required multiple rounds of fixing long lines, unused imports, blank lines, and indentation issues.
  - Some errors appeared in "chunks" as previous fixes revealed new ones.
- **Indentation & Mixed Spaces/Tabs:**
  - Encountered mixed indentation (tabs vs. spaces) in some return statements, which flake8 flagged.
- **Line Too Long in Arguments/Returns:**
  - Had to break up long argument lists and dictionary returns to comply with E501.
- **Final Success:**
  - After careful, incremental fixes, the backend now passes flake8 with zero errors, and the Jenkins pipeline is green.

---

**Lessons Learned:**
- CI/CD setup in real-world projects often requires troubleshooting environment and dependency issues.
- Linting and code quality gates are valuable but can be tedious to enforce on legacy or unformatted code.
- Incremental, testable changes and clear documentation make troubleshooting much easier. 