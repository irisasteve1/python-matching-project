# %%
"""
ideal_functions.py

Defines the IdealFunction SQLAlchemy ORM model for the ideal functions table,
which contains up to 50 ideal function columns.
"""
import sys
import os

# Add the root project folder to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from sqlalchemy import Column, Float, Integer
from src.models.functions_base import Base

# Ideal function table
class IdealFunction(Base):
    """
    SQLAlchemy ORM model for the ideal functions table.

    Columns:
        id (int): Primary key.
        x (float): X value.
        y1 ... y50 (float): Y values for each of the 50 ideal functions (dynamically generated as y1, y2, ..., y50).
    """
    __tablename__ = "ideal_functions"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    x = Column(Float, nullable=False)
    # y1 to y50 - load y1 to y50
    y_values = {f"y{i}": Column(Float) for i in range(1, 51)}
    locals().update(y_values)