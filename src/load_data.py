# %%
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd

from sqlalchemy.orm import sessionmaker
from src.models.train_data import TrainData
from src.models.ideal_functions import IdealFunction
from src.models.test_function import TestFunction
from src.models.functions_base import Base
import os


def load_data_into_db(engine, SessionLocal):
    """
    load train, ideal, and test data into the database

    Parameters:
        engine (sqlalchemy.engine.Engine): SQLAlchemy engine connected to the target database.
        SessionLocal (sessionmaker): SQLAlchemy sessionmaker bound to the engine.

    Returns:
        Exception: if there is an error during data loading or database operations.

    Notes:
        - Expects Excel files at '../data/train.xlsx', '../data/ideal.xlsx', and '../data/test.xlsx'.
        - Inserts data into TrainData, IdealFunction, and TestFunction tables.
    """
    session = SessionLocal()

    # Load excel files

    df_train = pd.read_excel("../data/train.xlsx")
    df_ideal = pd.read_excel("../data/ideal.xlsx")
    df_test = pd.read_excel("../data/test.xlsx")

    # Load train data
    for _, row in df_train.iterrows():
        session.add(TrainData(
            x=row['x'],
            y1=row['y1'],
            y2=row['y2'],
            y3=row['y3'],
            y4=row['y4']
        ))
    
    # Load ideal data
    for _, row in df_ideal.iterrows():
        session.add(IdealFunction(
            x=row['x'],
            **{f"y{i}": row[f"y{i}"] for i in range(1, 51)}

        ))

    # Load test
    for _, row in df_test.iterrows():
        session.add(TestFunction(
            x=row['x'],
            y=row['y']
        ))
    
    # Commit & close
    session.commit()
    session.close()


# %%