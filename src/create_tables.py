# %%
import sys
import os

# Add the root project folder to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.db import get_engine
from src.models.models import TrainData, IdealFunction, TestFunction
from src.models.functions_base import Base

def create_all_tables():
    """
    Create all database tables defined in the SQLAlchemy Base metadata.

    This includes TrainData, IdealFunction, and TestFunction tables.

    Parameters:
        None
    
    Returns:
        None

    Side Effects:
        Creates tables in the database specified by get_engine().
        prints a success message to the console.
    """
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")

if __name__ == "__main__":
    create_all_tables()

