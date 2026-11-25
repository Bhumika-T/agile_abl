import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")

    # SQLite by default for a zero-config local run; point DATABASE_URL at
    # MySQL to use the shared team database, e.g.
    # mysql+pymysql://root:password@localhost/library_db
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{BASE_DIR.as_posix()}/library.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
