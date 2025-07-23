# %%
import sys
import os

import tempfile
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the root project folder to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.best_fit import BestFit
from src.models.functions_base import Base
from src.save_utils import save_best_fit

def test_save_best_fit():
    """
    Unit test for the 'save_best_fit' function in save_utils.py.

    This test:
    - Creates a temporary in-memory SQLite database.
    - Initializes the schema (BestFit table).
    - Passes mock matched points to 'save_best_fit'.
    - Verifies that records are saved correctly to the DB.

    Ensures:
    - No data is lost during saving.
    - Data types and values are preserved.

    Raises:
        AssertionError: If any data is missing or does not match the expected values.
    """

    # Create a temporary SQLite DB
    with tempfile.NamedTemporaryFile(suffix=".db") as tmp:
        engine = create_engine(f"sqlite:///{tmp.name}")
        Base.metadata.create_all(engine) # create tables
        Session = sessionmaker(bind=engine)

        # Mock data to insert
        mock_points = [
            {'x': 1.0, 'y': 2.0, 'train_function': 'f1', 'ideal_function': 'f2', 'deviation': 0.01},
            {'x': 2.0, 'y': 3.5, 'train_function': 'f3', 'ideal_function': 'f4', 'deviation': 0.25}
        ]

        # Call the function to save data
        save_best_fit(mock_points, engine)

        # Check if records are saved
        session = Session()
        results = session.query(BestFit).all()

        assert len(results) == 2

        # Check both rows
        for point in mock_points:
            row = next(r for r in results if abs(r.x - point['x']) < 1e-6)
            assert abs(row.y - point['y']) < 1e-6
            assert row.train_function == point['train_function']
            assert row.ideal_function == point['ideal_function']
            assert abs(row.deviation - point['deviation']) < 1e-6

        session.close()
