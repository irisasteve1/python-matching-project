# %%
"""
db.py 

Database configuration using SQLAlchemy for the Programming with Python project.
Exposes utility functions to get the database engine and session for use across the project.
"""
import sys
import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.functions_base import Base


def get_database_url():
    """
    Builds the database URL for the results.db SQLite file.

    Returns:
        str: The database URL for the results.db SQLite in the database directory.
    """
    BASE_DIR = Path(__file__).resolve().parents[1]  # root project folder
    DB_PATH = BASE_DIR / "database" / "results.db"
    return f"sqlite:///{DB_PATH}"

def get_engine(url=None):
    """
    Create and return a SQLAlchemy engine instance.

    Parameters:
        url (str, optional): Custom database URL. if None, uses the default results.db path.

    Returns:
        sqlalchemy.engine.Engine: SQLAlchemy Engine instance connected to the database.
    """

    db_url = url or get_database_url()
    return create_engine(db_url, connect_args={"check_same_thread": False})

def get_session(engine):
    """
    Return a configured SQLAlchemy sessionmaker bound to the provided engine.

    Parameters:
        engine (sqlalchemy.engine.Engine): SQLAlchemy Engine instance.

    Returns:
        sqlalchemy.orm.session.sessionmaker: Configured sessionmaker for database sessions.
    """
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)

