from pydantic import BaseSettings
import os


class CommonSettings(BaseSettings):
    APP_NAME: str = ""
    DEBUG_MODE: bool = True


class ServerSettings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000


class DatabaseSettings(BaseSettings):
    DB_LOGIN: str = os.environ['db_login'] if "db_login" in os.environ else "admin"
    DB_PASSWORD: str = os.environ['db_password'] if "db_password" in os.environ else "admin"
    DB_URL: str = f"mongodb+srv://{DB_LOGIN}:{DB_PASSWORD}@cluster0.3g8z5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    DB_NAME: str = "HemoDB"
    DB_COLL: str = "Temperatures"
    DB_COLL_TEST: str = "TemperaturesTest"


class Settings(CommonSettings, ServerSettings, DatabaseSettings):
    pass


settings = Settings()
