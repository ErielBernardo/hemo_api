from pydantic import BaseSettings
import os


class AppSettings(BaseSettings):
    APP_NAME: str = "HemoAPI"
    DESCRIPTION: str = """HemoApp API helps hospitals to control and monitor blood components. 🚀🩸🩸"""
    CONTACT: dict = {
        "name": "Eriel Bernardo Albino",
        "url": "https://www.linkedin.com/in/erielbernardo/",
        "email": "erielberrnardo@gmail.com",
    }
    VERSION: str = "0.1.0"
    DEBUG_MODE: bool = True


class ServerSettings(BaseSettings):
    HOST: str = "localhost"
    PORT: int = 8000


class DatabaseSettings(BaseSettings):
    DB_LOGIN: str = os.environ['db_login'] if "db_login" in os.environ else "admin"
    DB_PASSWORD: str = os.environ['db_password'] if "db_password" in os.environ else "admin"
    DB_URL: str = f"mongodb+srv://{DB_LOGIN}:{DB_PASSWORD}@cluster0.3g8z5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    DB_NAME: str = "HemoDB"
    DB_COLL: str = "Temperatures"
    DB_COLL_TEST: str = "TemperaturesTest"


class Settings(AppSettings, ServerSettings, DatabaseSettings):
    pass


settings = Settings()
