from pydantic import BaseModel

class RepoRequest(BaseModel):
    url: str

class ReadmeResponse(BaseModel):
    markdown: str