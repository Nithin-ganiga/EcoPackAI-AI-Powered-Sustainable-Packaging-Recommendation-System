"""This file centralizes environment-based configuration so the rest of the backend can read database settings from one reliable place without repeating parsing logic."""

import os
from dotenv import load_dotenv


load_dotenv()


class Config:
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_DB = os.getenv("MYSQL_DB", "ecopackai_db")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))


config = Config()
