from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Tramplin API"
    api_prefix: str = "/api/v1"

    secret_key: str = "change-me"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7

    database_url: str = "postgresql+psycopg://tramplin:tramplin@postgres:5432/tramplin"
    cors_origins: str = "http://localhost:3000"

    nominatim_url: str = "https://nominatim.openstreetmap.org/search"
    nominatim_user_agent: str = "tramplin-app/1.0"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
