# %%
"""
train_data.py

Defines the TrainData SQLAlchemy ORM model for the training functions table.
"""
import sys
import os

# Add the root project folder to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from sqlalchemy import Column, Float, Integer, String
from src.models.functions_base import Base

# Train function table
class TrainData(Base):
    """
    SQLAlchemy ORM model for the training functions table.

    Columns:
        id (int): Primary key.
        x (float): X value.
        y1 (float): Y value for training function 1.
        y2 (float): Y value for training function 2.
        y3 (float): Y value for training function 3.
        y4 (float): Y value for training function 4.
    """
    __tablename__ = "train_functions"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    x = Column(Float)
    y1 = Column(Float)
    y2 = Column(Float)
    y3 = Column(Float)
    y4 = Column(Float)