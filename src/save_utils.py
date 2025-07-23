# %%
"""
save_utils.py

Utility function for saving matched test points to the database using SQLAlchemy ORM.
"""
import sys
from pathlib import Path
from sqlalchemy.orm import sessionmaker

# Add the parent directory to the path so we can import from src
sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.models.best_fit import BestFit

def save_best_fit(mapped_points, engine):
    """
    Saves matched test points to the database.

    Parameters:
    - mapped_points (list of dict): each dict must contain the keys
     'x', 'y', 'train_function', 'ideal_function', and 'deviation'.
     engine (sqlalchemy.engine.Engine): SQLAlchemy engine connected to the target database.

    Returns:
    - None

    Raises:
        Exception: If there is an error during the database transaction.
    """
    Session = sessionmaker(bind=engine)
    db = Session()
    try:
        for point in mapped_points:
            record = BestFit(
                x=point['x'],
                y=point['y'],
                train_function=point['train_function'],
                ideal_function=point['ideal_function'],
                deviation=point['deviation']
            )
            db.add(record)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

