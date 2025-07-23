#%%
"""
data_handler.py

Provides object-oriented data handler classes for loading and saving 
training, test, and ideal function data to the database using SQLAlchemy.
"""

from IPython.display import display   # for notebook-friendly display
import sys
from pathlib import Path
import os
# ------------------ Internal ------------------ #
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.models.train_data import TrainData
from src.models.ideal_functions import IdealFunction
from src.models.test_function import TestFunction
from src.exceptions import DataLoadError
import pandas as pd


class BaseDataHandler:
    """
    Abstract base class for data handlers.
    
    Provides an interface for loading and saving data to the database.
    Subclasses must implement the load_data and save_data methods.

    Args:
        session (Session): SQLAlchemy session for database operations.
    """
    def __init__(self, session):
        """
        Initializes the data handler with a database session.

        Args:
            session (Session): SQLAlchemy session for database operations.
        """
        self.session = session

    def load_data(self, filepath):
        """
        Load data from a file. To be implemented by subclasses.

        Args:
            filepath (str): Path to the data file.

        Raises:
            NotImplementedError("Subclasses must implement this method.")
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def save_data(self, data):
        """
        Save data to the database. To be implemented by subclasses.

        Args:
            data (pd.DataFrame): Data to be saved.
        
        Raises:
            NotImplemetedError: if not implemented in subclass.
        """
        raise NotImplementedError("Subclasses must implement this method.")

class TrainDataHandler(BaseDataHandler):
    """
    Data handler for training data.

    Loads training data from an excel file and saves it to the database.
    Inherits from BaseDataHandler.
    """
    def load_data(self, filepath):
        """
        Loads training data from an Excel file.

        Args:
            filepath(str): Path to the Excel file.

        Returns:
            pd.DataFrame: Dataframe containing the training data.

        Raises:
            DataLoadError: if the file cannot be loaded.
        """
        try:
            df = pd.read_excel(filepath)
            return df
        except Exception as e:
            raise DataLoadError(f"Failed to load training data from {filepath}: {e}")

    def save_data(self, data):
        """
        Saves training data to the database.

        Args:
            data (pd.DataFrame): Dataframe containing the training data.

        Raises:
            DataLoadError: If the data cannot be saved to the database.
        """
        try:
            for _, row in data.iterrows():
                self.session.add(TrainData(
                    x=row['x'],
                    y1=row['y1'],
                    y2=row['y2'],
                    y3=row['y3'],
                    y4=row['y4']
                ))
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise DataLoadError(f"Failed to save training data to database: {e}") 


class TestDataHandler(BaseDataHandler):
    """
    Data handler for test data.

    Loads test data from an Excel file and saves it to the database.
    Inherits from BaseDataHandler.
    """
    def load_data(self, filepath):
        """
        Loads test data from an Excel file.

        Args:
            filepath (str): Path to the excel file.

        Returns:
            pd.DataFrame: DataFrame containing the test data.

        Raises:
            DataLoadError: If the file cannot be loaded.
        """
        try:
            df = pd.read_excel(filepath)
            return df
        except Exception as e:
            raise DataLoadError(f"Failed to load test data from {filepath}: {e}")

    def save_data(self, data):
        """
        Saves test data to the database.

        Args:
            data (pd.DataFrame): DataFrame containing the test data.

        Raises:
            DataLoadError: If the data cannot be saved to the database.
        """
        try:
            for _, row in data.iterrows():
                self.session.add(TestFunction(
                    x=row['x'],
                    y=row['y'],
                ))
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise DataLoadError(f"Failed to save test data to database: {e}")


class IdealDataHandler(BaseDataHandler):
    """
    Data handler for ideal function data. 

    Loads ideal function data from an excel file and saves it to the database.
    Inherits from BaseDataHandler.
    """
    def load_data(self, filepath):
        """
        Loads ideal function data from an excel file.

        Args:
            filepath (str): Path to the excel file.

        Returns:
            pd.DataFrame: DataFrame containing the ideal function data.

        Raises:
            DataLoadError: If the file cannot be loaded.
        """
        try:
            df = pd.read_excel(filepath)
            return df
        except Exception as e:
            raise DataLoadError(f"Failed to load ideal data from {filepath}: {e}")
        
    def save_data(self, data):
        """
        Saves ideal function data to the database.

        Args:
            data (pd.DataFrame): DataFrame containing the ideal function data.

        Raises:
            DataLoadError: If the data cannot be saved to the database.
        """
        try:
            for _, row in data.iterrows():
                # Dynamic function
                y_values = {f"y{i}": row[f"y{i}"] for i in range(1, 5)}
                self.session.add(IdealFunction(
                    x=row['x'],
                    **y_values
                ))
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise DataLoadError(f"Failed to save ideal data to database: {e}")
