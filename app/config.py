from dotenv import load_dotenv
import os

load_dotenv()

ENV = os.environ.get("FLASK_ENV", "development").lower()


class BaseConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY", "secret123")
    DEBUG = False
    TESTING = False
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 15))
    REFRESH_TOKEN_EXPIRE_DAYS = int(os.environ.get("REFRESH_TOKEN_EXPIRE_DAYS", 7))

    STARROCKS_HOST = os.environ.get("STARROCKS_HOST", "localhost")
    STARROCKS_PORT = int(os.environ.get("STARROCKS_PORT", 9030))
    STARROCKS_DATABASE = os.environ.get("STARROCKS_DATABASE", "ventas_db")
    STARROCKS_USER = os.environ.get("STARROCKS_USER", "root")
    STARROCKS_PASSWORD = os.environ.get("STARROCKS_PASSWORD", "")


class DevelopmentConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True


class ProductionConfig(BaseConfig):
    pass


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}

ActiveConfig = config.get(ENV, DevelopmentConfig)
