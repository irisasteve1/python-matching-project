# %%
"""
functions_base.py

Defines the SQLAlchemy declarative base (Base) for all ORM models in the project.
All model classes should inherit from this Base.
"""
from sqlalchemy.orm import declarative_base

Base = declarative_base()

