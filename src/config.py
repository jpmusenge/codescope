import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# model configurations
AVAILABLE_MODELS = {
    "claude": "anthropic:claude-sonnet-4-20250514",
    "gpt4": "openai:gpt-4o",
    "gpt4-mini": "openai:gpt-4o-mini",
    "gemini": "google:gemini-2.0-flash",
}

DEFAULT_MODEL = "gpt4-mini"
# agent configuration
# how many tool-use turns the agent can take
MAX_TURNS = 25

SUPPORTED_EXTENSIONS = {
    ".py", ".js", ".jsx", ".ts", ".tsx",
    ".java", ".c", ".cpp", ".h", ".hpp",
    ".go", ".rs", ".rb", ".php",
    ".html", ".css", ".json", ".yaml", ".yml",
    ".md", ".txt",
}

REPORTS_DIR = Path("./reports")