from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Database
    db_url: str = "postgresql+psycopg://postgres:postgres@db:5432/meeting_insights"
    
    # Redis
    redis_url: str = "redis://redis:6379/0"
    
    # S3
    s3_endpoint: str = "http://minio:9000"
    s3_access_key: str = "minioadmin"
    s3_secret_key: str = "minioadmin"
    s3_bucket_audio: str = "meeting-audio"
    s3_bucket_transcripts: str = "meeting-transcripts"
    s3_region: str = "us-east-1"
    
    # JWT
    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    
    # CORS
    allowed_origins: str = "http://localhost:5173,http://localhost:3000"
    
    # LLM Provider
    llm_provider: str = "mock"
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    
    # Whisper
    whisper_enabled: bool = True
    whisper_model: str = "base"
    
    # Redaction
    redaction_enabled: bool = True
    
    # Integrations
    slack_bot_token: str = ""
    jira_base_url: str = ""
    jira_email: str = ""
    jira_api_token: str = ""
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # Worker
    worker_concurrency: int = 4
    
    @property
    def cors_origins(self) -> List[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

