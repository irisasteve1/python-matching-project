# %%
"""
best_fit.py

Defines the BestFit SQLAlchemy ORM model for storing matched test points,
including their corresponding training and ideal functions and deviation values.
"""
import sys
import os

# Add the root project folder to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from sqlalchemy import Column, Float, Integer, String
from src.models.functions_base import Base

class BestFit(Base):
    """
    SQLAlchemy ORM model for the best_fit_points table.

    Columns:
        id (int): Primary key.
        x (float): X value of the test point.
        y (float): Y value of the test point.
        train_function (str): Name of the matched training function.
        ideal_function (str): Name of the matched ideal function.
        deviation (float): Deviation from the ideal function.
    """
    __tablename__ = "best_fit_points"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)
    train_function = Column(String, nullable=False)
    ideal_function = Column(String,nullable=False)
    deviation = Column(Float, nullable=False)