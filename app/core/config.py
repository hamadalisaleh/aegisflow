from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "AegisFlow"
    DATABASE_URL: str = (
        "postgresql://aegis_user:aegis_password@localhost:5432/aegisflow_db"
    )
    SECRET_KEY: str = (
        "supersecretkey_for_development_only_change_in_production"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()