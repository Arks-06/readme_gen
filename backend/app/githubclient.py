import requests
import base64
from app.config import Config

def parse_repo_url(url: str):
    """
    Safely extracts the owner and repo name, handling trailing slashes 
    and .git extensions perfectly.
    """
    clean_url = url.strip().rstrip('/')
    if clean_url.endswith('.git'):
        clean_url = clean_url[:-4]
    
    parts = clean_url.split('/')
    return parts[-2], parts[-1]

def get_recursive_repo_structure(owner: str, repo: str, branch: str = "main") -> str:
    """
    Fetches the absolute entire repository tree recursively in a single API call.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
    headers = {"Accept": "application/vnd.github+json"}
    
    if Config.GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {Config.GITHUB_TOKEN}"
        
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        if branch == "main":
            return get_recursive_repo_structure(owner, repo, branch="master")
        return "Structure could not be fetched."
        
    tree_data = response.json().get("tree", [])
    
    structure_lines = [f"{repo}/"]
    for item in tree_data:
        path = item["path"]

        if path.endswith("__init__.py"):
            continue

        path_parts = path.split("/")
        indent = "    " * (len(path_parts) - 1)
        
        if item["type"] == "tree":
            structure_lines.append(f"{indent}├── {path_parts[-1]}/")
        else:
            structure_lines.append(f"{indent}├── {path_parts[-1]}")
            
    return "\n".join(structure_lines)

def get_repo_context(url: str) -> str:
    owner, repo = parse_repo_url(url)
    headers = {"Authorization": f"Bearer {Config.GITHUB_TOKEN}"}
    
    full_tree_structure = get_recursive_repo_structure(owner, repo)
    
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents"
    response = requests.get(api_url, headers=headers)
    
    if response.status_code != 200:
        raise Exception("Failed to fetch repo. Check URL or GitHub token.")
    
    contents = response.json()
    
    repo_context = f"Repository: {owner}/{repo}\n\n"
    repo_context += f"--- FULL PROJECT STRUCTURE ---\n{full_tree_structure}\n\n"
    repo_context += "--- CRITICAL FILE CONTENTS ---\n"
    
    target_files = [
        'README.md', 'package.json', 'requirements.txt', 
        'main.py', 'app.js', 'index.js', 'pyproject.toml', 'uv.lock'
    ]
    
    for item in contents:
        if item['type'] == 'file' and item['name'] in target_files:
            file_resp = requests.get(item['url'], headers=headers).json()
            if 'content' in file_resp:
                decoded_content = base64.b64decode(file_resp['content']).decode('utf-8')
                repo_context += f"\nFile: {item['name']}\n{decoded_content[:2000]}\n"

    return repo_context