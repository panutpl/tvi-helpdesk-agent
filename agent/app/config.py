from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# config.py อยู่ที่ agent/app/config.py -> ขึ้นไป 3 ชั้นได้ root ของ repo
# ผูก path กับตำแหน่งไฟล์โค้ด ไม่ใช่กับที่ที่รันคำสั่ง
# จะได้รันจากโฟลเดอร์ไหนก็ได้ผลเหมือนกัน
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        extra="ignore",
    )

    # LLM
    anthropic_api_key: str = ""
    anthropic_base_url: str = "https://api.anthropic.com"
    llm_model: str = "claude-sonnet-4-5"
    llm_max_tokens: int = 1024
    llm_temperature: float = 0.0

    # Embedding
    embedding_model: str = "BAAI/bge-m3"
 
    # Retrieval
    knowledge_base_dir: str = str(PROJECT_ROOT / "knowledge-base")
    chroma_persist_dir: str = str(PROJECT_ROOT / ".chroma")
    chroma_collection: str = "techcorp_kb"
    retrieval_top_k: int = 5

    # Mock API
    mock_api_base_url: str = "http://localhost:8080/api"
    mock_api_token: str = "techcorp-mock-token-2025"
    mock_api_timeout: float = 10.0

    # Agent
    memory_max_turns: int = 5
    agent_max_iterations: int = 5
    log_level: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    """อ่าน .env ครั้งเดียวแล้ว cache ไว้ ทุกโมดูลเรียกตัวนี้"""
    return Settings()
