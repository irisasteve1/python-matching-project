# %%
"""
test_create_tables.py

Unit tests for verifying that all required database tables are created correctly
using SQLAlchemy ORM models and the Base metadata.
"""
import sys
import os
import sqlite3
import tempfile
from sqlalchemy import inspect, create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.train_data import TrainData
from src.models.ideal_functions import IdealFunction
from src.models.test_function import TestFunction
from src.models.functions_base import Base

def test_create_all_tables():
    """
    Test that all expected tables are created in the temporary SQLite database.

    Steps:
        - Creates a temporary SQLite database.
        - Uses SQLAlchemy Base metadata to create all tables.
        - Asserts that the tables for TrainData, IdealFunction, and TestFunction exist.
        - Cleans up the  temporary database file.

    Raises:
        AssertionError: If any expected table is missing.
    """
    # Setup: create a temporary SQLite database
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        test_db_path = tmp.name

    test_engine = create_engine(f"sqlite:///{test_db_path}")
    Session = sessionmaker(bind=test_engine)
    Base.metadata.drop_all(bind=test_engine)
    # Act: create tables
    Base.metadata.create_all(bind=test_engine)

    # Assert: check tables exist
    inspector = inspect(test_engine)
    tables = inspector.get_table_names()

    expected_tables = [
        TrainData.__tablename__,
        IdealFunction.__tablename__,
        TestFunction.__tablename__,
        ]
    for table in expected_tables:
        assert table in tables, f"Missing table: {table}"

    test_engine.dispose()
    os.remove(test_db_path)


# %%

