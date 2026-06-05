from groq import Groq
from app.config import Config

client = Groq(api_key=Config.GROQ_API_KEY)

def generate_readme(repo_context: str) -> str:
    system_prompt = """
    You are an expert developer. Based on the provided repository structure and file contents, 
    generate a comprehensive, professional README.md file. 
    
    Include the following standard sections: 
    Title, Description, Features, Project Structure, Configuration, Prerequisites, Database Setup (if applicable), Installation, Usage, and License.
    
    CRITICAL INSTRUCTIONS:
    1. Project Structure: Use the provided visual tree structure. Do not invent files that are not present.
    2. Environment Variables: If you detect configuration via environment variables, add a 'Configuration' section detailing the `.env` setup.
    3. The 'uv' Package Manager Lifecycle: If this is a Python project using 'uv' (indicated by pyproject.toml or uv.lock), explicitly write out the full setup lifecycle:
       - Installation: Instruct the user to navigate into the respective folder and run `uv sync` to install dependencies.
       - Execution: Do NOT use naked commands like `uv run`. You must specify the target.
         * If it is a Reflex frontend, the command MUST be `uv run reflex run`.
         * If it is a FastAPI backend, the command MUST be `uv run fastapi dev main.py --port 8080` (or the detected entry point).
    4. Dynamic Database Setup: Analyze the files to detect if a database is used. 
       - If a database is detected AND a `docker-compose.yml` is present, include a 'Database Setup' section with the exact Docker commands to spin it up (e.g., `docker compose up -d`).
       - If a database is detected but NO Docker files are present, include a 'Database Setup' section instructing the user to ensure their local database (specify the detected type, e.g., PostgreSQL, MongoDB) is running and to update the connection string in the `.env` file.
    5. Modern Python: Ensure Python prerequisites specify Python 3.10 or higher.
    
    Format the output STRICTLY as valid Markdown. Do not include introductory conversational text.
    """
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Here is the repository context:\n{repo_context}"}
            ],
            model=Config.GROQ_MODEL,
            temperature=0.3,
        )
        return chat_completion.choices[0].message.content
        
    except Exception as e:
        # EXPLICIT DEBUG LOG:
        print(f"--- GROQ CRASH ERROR: {type(e).__name__} - {str(e)} ---")
        raise Exception(f"Groq failed: {str(e)}")