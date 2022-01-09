from pydantic import BaseSettings


class CommonSettings(BaseSettings):
    app_name: str = "FASTAPI"
    debug_mode: bool = False

    class Config:
        env_file = ".env"


class ServerSettings(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8000


class DatabaseSettings(BaseSettings):
    db_url: str
    db_name: str


class Settings(CommonSettings, ServerSettings, DatabaseSettings):
    pass


settings = Settings()
