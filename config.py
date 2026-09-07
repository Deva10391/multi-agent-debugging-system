import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")
REPO_PATH = os.getenv("REPO_PATH", "./repo")
FILE_PATH = os.getenv("FILE_PATH", "file.py")
LLM_RETRY_ATTEMPTS = int(os.getenv("LLM_RETRY_ATTEMPTS", "4"))
MAX_DEBUG_ATTEMPTS = int(os.getenv("MAX_DEBUG_ATTEMPTS", "5"))
SANDBOX_TIMEOUT_SECONDS = int(os.getenv("SANDBOX_TIMEOUT_SECONDS", "30"))
DOCKER_IMAGE = os.getenv("DOCKER_IMAGE", "debugger-sandbox:latest")
LLM_TEMPERATURE = 0

"""
centralized settings
"""