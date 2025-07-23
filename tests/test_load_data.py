# %%
"""
test_load_data.py

Unit test for verifying that training, ideal, and test data are loaded into the database 
correctly using the load_data_into_db function. checks both row counts and actual values.
"""
import sys
import pytest 
import tempfile
import os
from unittest.mock import patch
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.train_data import TrainData
from src.models.ideal_functions import IdealFunction
from src.models.test_function import TestFunction
from src.models.functions_base import Base

from src.load_data import load_data_into_db

def test_load_data_into_db():
    """
    Test that training, ideal, and test data are loaded into the database correctly.

    Steps:
        - Prepares mock DataFrames for training, ideal, and test data.
        - Patches pandas.read_excel to return these DataFrames.
        - Loads data into a temporary SQLite database using load_data_into_db.
        - Asserts that the correct number of rows are inserted for each table.
        - Checks that the actual values in the TrainData table match the mock data.

    Raises:
        AssertionError: If any data is missing or does not match the expected values.
    """
    # prepare mock data
    df_train = pd.DataFrame({
        'x':[1],
        'y1':[10],
        'y2':[20],
        'y3':[30],
        'y4':[40] 
    })
    df_ideal = pd.DataFrame({
        'x': [1],
        **{f'y{i}': [i * 1.0] for i in range(1, 51)}
    })
    df_test = pd.DataFrame({
        'x': [1],
        'y': [100.0]
    })


    with tempfile.NamedTemporaryFile(suffix=".db") as tmp_db:
        engine = create_engine(f"sqlite:///{tmp_db.name}")
        Base.metadata.create_all(engine)
        SessionLocal = sessionmaker(bind=engine)

        # patch pd.read_excel to return our mock data in sequence
        with patch('pandas.read_excel', side_effect=[df_train, df_ideal, df_test]):
            load_data_into_db(engine, SessionLocal)

        # Verify data was inserted
        session = SessionLocal()

        assert session.query(TrainData).count() == 1
        assert session.query(IdealFunction).count() == 1
        assert session.query(TestFunction).count() == 1

        # Check actual row values
        train_row = session.query(TrainData).first()
        assert train_row.x == 1
        assert train_row.y1 == 10

        print(f"x={train_row.x}, y1={train_row.y1}")  # Debug print
        session.close()
        
    

