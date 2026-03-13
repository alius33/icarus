from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://icarus:icarus_local@localhost:5432/icarus"
    SYNC_DATABASE_URL: str = "postgresql://icarus:icarus_local@localhost:5432/icarus"
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:3001"]
    DATA_ROOT: str = "."
    SECRET_KEY: str = "change-me-in-production"
    AUTH_ENABLED: bool = False  # Set to True in production
    MAX_ATTACHMENT_SIZE: int = 25 * 1024 * 1024  # 25 MB
    MAX_ATTACHMENTS_PER_TRANSCRIPT: int = 10

    class Config:
        env_file = ".env"


settings = Settings()
