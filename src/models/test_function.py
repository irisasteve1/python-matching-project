# %%
"""
test_functions.py

Defines the TestFunction SQLAlchemy ORM model for the test functions table.
"""
import sys
import os

# Add the root project folder to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from sqlalchemy import Column, Float, Integer, String
from src.models.functions_base import Base

# Test function table
class TestFunction(Base):
    """
    SQLAlchemy ORM model for the test functions table.

    Columns:
        id (int): Primary key.
        x (float): X value of the test point.
        y (float): Y value of the test point.
        ideal_function (str, optional): Name of the matched ideal function.
        deviation (float, optional): Deviation from the ideal function.
    """
    __tablename__ = "test_functions"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)
    ideal_function = Column(String, nullable=True)
    deviation = Column(Float, nullable=True)
    