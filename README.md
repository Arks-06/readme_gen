# Arks-06/readme_gen
## Description
Writing documentation is often the most tedious part of shipping code.
**readme_gen** is an AI-powered documentation agent that automatically generates comprehensive, `README.md` files for any public GitHub repository. 
By analyzing a project's directory structure, file contents, and tech stack, it eliminates the manual overhead of writing documentation from scratch. The system is built on a fully decoupled architecture: a high-performance **FastAPI** backend orchestrates the AI pipeline using **Groq**, while a reactive **Reflex** web frontend provides a seamless user interface for generating and previewing the markdown.

## Features
* AI-driven content generation that analyzes source code to write intelligent documentation.
* Fully decoupled architecture with a high-performance backend and a reactive web UI.

## Project Structure
```markdown
readme_gen/
├── backend/
    ├── .python-version
    ├── README.md
    ├── app/
        ├── agent.py
        ├── config.py
        ├── githubclient.py
        ├── route.py
        ├── schema.py
    ├── main.py
    ├── pyproject.toml
    ├── requirements.txt
    ├── uv.lock
├── frontend/
    ├── .python-version
    ├── README.md
    ├── assets/
        ├── favicon.ico
    ├── frontend/
        ├── frontend.py
    ├── main.py
    ├── pyproject.toml
    ├── reflex.lock/
        ├── bun.lock
        ├── package.json
    ├── rxconfig.py
    ├── uv.lock
```

## Tech Stack
* **Backend:** FastAPI, Python 3.10+, uv
* **Frontend:** Reflex 
* **AI Engine:** Groq

## Configuration
The project uses environment variables for configuration. To set up the environment variables, create a `.env` file in the root directory of the project and add the necessary variables.
```markdown
GITHUB_TOKEN=your_github_personal_access_token
AI_API_KEY=your_llm_api_key_here
```

## Prerequisites
* Python 3.10 or higher
* uv package manager

## Database Setup
No database setup is required for this project.

## Installation
To install the dependencies, navigate to the `backend` and `frontend` directories and run the following commands:
```bash
# Backend
cd backend
uv sync

# Frontend
cd frontend
uv sync
```

## Usage
To run the backend, navigate to the `backend` directory and run the following command:
```bash
uv run fastapi dev main.py --port 8080
```
To run the frontend, navigate to the `frontend` directory and run the following command:
```bash
uv run reflex run
```

## License
No license information is available for this project.