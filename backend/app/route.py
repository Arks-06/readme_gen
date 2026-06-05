from fastapi import APIRouter, HTTPException
from app.schema import RepoRequest, ReadmeResponse
from app.githubclient import get_repo_context
from app.agent import generate_readme

router = APIRouter()

@router.post("/api/generate", response_model=ReadmeResponse)
def generate_readme_endpoint(request: RepoRequest):
    try:
        repo_context = get_repo_context(request.url)
        
        readme_md = generate_readme(repo_context)
        
        return {"markdown": readme_md}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))