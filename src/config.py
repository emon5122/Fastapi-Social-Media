from pydantic import BaseSettings
import os


class Settings(BaseSettings):
    SECRET_KEY : str = os.getenv("Secret_Key")
    ALGORITHM: str = os.getenv("Algorithm")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("TokenExpire")
    DB_USER: str =os.getenv("DBUSER")
    DB_PASS: str =os.getenv("DBPASS")
    DB_HOST: str =os.getenv("DBHOST")
    DB_NAME: str =os.getenv("DBNAME")

settings= Settings()