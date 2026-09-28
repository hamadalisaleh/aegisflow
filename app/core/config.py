from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AegisFlow"
    DATABASE_URL: str = "sqlite:///./aegisflow.db"
    SECRET_KEY: str = "supersecretkey_for_development_only_change_in_production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    class Config:
        env_file = ".env"

<<<<<<< HEAD
settings = Settings()
=======
settings = Settings()
>>>>>>> 9c4d87fab85b1e106f349f81a2e7ae6eee30e18b
