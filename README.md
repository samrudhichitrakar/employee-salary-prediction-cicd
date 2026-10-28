# Employee Salary Prediction — CI/CD and Monitoring

**Student:** Samrudhi Shivaji Chitrakar  
**Roll No.:** 12  
**PRN:** 2324000303  
**Course:** ML DevOps Laboratory (UDSPC0732), A.Y. 2026–27

## Problem statement
Build a small Flask web application that estimates annual employee salary from years of experience and education level. Use Git and GitHub for version control, Jenkins for automated testing and Docker image builds, Docker for containerization, and `/health` plus `/metrics` endpoints for basic monitoring.

## Important note
The application uses a tiny synthetic dataset embedded in `app.py` for classroom demonstration only. Predictions are illustrative, not validated salary advice, and must not be used for actual hiring or compensation decisions.

## Run locally on Windows PowerShell
```powershell
python --version
git --version
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest -q
python app.py
```
Open `http://127.0.0.1:5000`. Health endpoint: `http://127.0.0.1:5000/health`. Metrics endpoint: `http://127.0.0.1:5000/metrics`.

## Build and run with Docker
Make sure Docker Desktop is running:
```powershell
docker --version
docker build -t employee-salary-prediction .
docker run --rm -p 5000:5000 employee-salary-prediction
```
Open `http://localhost:5000`.

## Publish to GitHub
1. Create a **new empty repository** on GitHub named `employee-salary-prediction-cicd`. Do not add README/license/gitignore there because this folder already contains files.
2. In PowerShell, change directory to this extracted folder:
```powershell
git init
git add .
git commit -m "Initial employee salary prediction app"
git branch -M main
git remote add origin https://github.com/YOUR-GITHUB-USERNAME/employee-salary-prediction-cicd.git
git push -u origin main
```
Replace `YOUR-GITHUB-USERNAME` with your actual GitHub username. Authenticate when Git prompts you.

## Jenkins
The included `Jenkinsfile` is for a Jenkins agent running on Windows with Python, Git, and Docker CLI available. Create a Pipeline job, configure it to use this GitHub repository, and select “Pipeline script from SCM” with `Jenkinsfile` as the script path. Run the job and verify that tests pass and the Docker image builds. The Jenkins service account must have permission to use Docker.

## Git commands for verification
```powershell
git status
git log --oneline
git remote -v
```

## GitHub repository URL
Add your actual repository URL here after creating and pushing the repository.
