from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    DB_URL: str = "postgresql+asyncpg://postgres:rootxvk9@localhost:5432/fastapi_test"
    PROJECT_NAME: str = "FastAPI SQLModel Async"
    VERSION: str = "0.1.0"

    class Config:
        case_sensitive = True


settings: Settings = Settings()
