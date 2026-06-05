import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    # Using Llama 3 on Groq for blazing fast generation
    GROQ_MODEL = "llama3-70b-8192"


import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL = "llama-3.3-70b-versatile" 

print(f"--- DEBUG: GitHub Token Loaded? {bool(Config.GITHUB_TOKEN)} ---")
print(f"--- DEBUG: Groq Token Loaded? {bool(Config.GROQ_API_KEY)} ---") 