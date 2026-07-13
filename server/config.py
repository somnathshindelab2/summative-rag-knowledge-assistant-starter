import os
from dotenv import load_dotenv

load_dotenv()


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def _resolve_path(value: str | None, default: str) -> str:
    """Resolve relative paths against the server directory."""
    if not value:
        return os.path.abspath(os.path.join(BASE_DIR, default.lstrip("./")))

    if os.path.isabs(value):
        return value

    return os.path.abspath(os.path.join(BASE_DIR, value))


class Config:
    """Application configuration loaded from environment variables."""

    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    GENERATION_MODEL = os.getenv("GENERATION_MODEL", "llama3.2")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")

    CHROMA_PATH = _resolve_path(os.getenv("CHROMA_PATH"), "./chroma_db")
    COLLECTION_NAME = os.getenv("COLLECTION_NAME", "knowledge_assistant")
    KNOWLEDGE_BASE_PATH = _resolve_path(os.getenv("KNOWLEDGE_BASE_PATH"), "./knowledge_base")

    TOP_K = int(os.getenv("TOP_K", "3"))
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.2"))

    CLIENT_ORIGIN = os.getenv("CLIENT_ORIGIN", "http://localhost:5173")
