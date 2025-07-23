# %%
"""
main.py

Main entry point for the Programming with Python project.

- Loads training data, ideal, and test data using OOP data handlers.
- Finds best-fit ideal functions for training data.
- Maps test data points to ideal functions based on deviation thresholds.
- Saves results to the database.
- Visualizes results using matplotlib
"""
# --------------------------------------------------------------
# Imports
# --------------------------------------------------------------

# ------------------ Standard Library ------------------ #
from IPython.display import display   # for notebook-friendly display
import sys
from pathlib import Path
import os

# ------------------ Standard Library ------------------ #
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from sqlalchemy import create_engine


from src.db import get_engine, get_session

engine = get_engine()
SessionLocal = get_session(engine)
session = SessionLocal()

base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "data")
db_dir = os.path.join(base_dir, "database")

# Make sure the directory exists
os.makedirs(db_dir, exist_ok=True)

# ------------------ Internal ------------------ #
sys.path.append(str(Path(__file__).resolve().parent.parent))

#from src.db import Base, engine             # DB connection and base metadata
from src.models.best_fit import BestFit              # ORM model
from src.save_utils import save_best_fit    # DB save utility

from src.visualize import (
    plot_best_matches,
    plot_test_vs_ideal,
    plot_deviations,
)

# %%
# --------------------------------------------------------------
# DB Setup
# --------------------------------------------------------------

functions_engine = create_engine(f"sqlite:///{os.path.join(db_dir, 'functions.db')}")
results_engine = create_engine(f"sqlite:///{os.path.join(db_dir, 'results.db')}")

FunctionsSessionLocal = get_session(functions_engine)
ResultsSessionLocal = get_session(results_engine)

functions_session = FunctionsSessionLocal()
results_session = ResultsSessionLocal()

# %%
# --------------------------------------------------------------
# Data Loading
# --------------------------------------------------------------
from src.data_handler import TrainDataHandler, IdealDataHandler, TestDataHandler
from src.exceptions import DataLoadError

# Instanctiate handlers
train_handler = TrainDataHandler(functions_session)
ideal_handler = IdealDataHandler(functions_session)
test_handler = TestDataHandler(functions_session)

# Load data using handlers
try:
    training_data = train_handler.load_data(os.path.join(data_dir, "train.xlsx"))
    ideal_data = ideal_handler.load_data(os.path.join(data_dir, "ideal.xlsx"))
    test_data = test_handler.load_data(os.path.join(data_dir, "test.xlsx"))
except DataLoadError as e:
    print(f"Error loading data: {e}")
    sys.exit(1)

# save data to database 
train_handler.save_data(training_data)
ideal_handler.save_data(ideal_data)
test_handler.save_data(test_data)


# --------------------------------------------------------------
# Function: Find Best Ideal Functions 
# --------------------------------------------------------------
def find_best_ideal_functions(training_data, ideal_data):
    """
    Finds the best matching ideal function for each training function using the least squares method.

    Args:
        training_data (pd.DataFrame): Dataframe containing x and training function columns.
        ideal_data (pd.DataFrame): DataFrame containing x and ideal function columns.

    Returns:
        tuple:
            - best_matches (dict): Mapping of training function column to the best ideal match. 
            - max_deviations (dict): Maximum deviation for each matched ideal function.

    """
    best_matches = {}
    max_deviations = {}
    train_x = training_data['x']

    for train_col in training_data.columns:
        if train_col == 'x':
            continue

        train_y = training_data[train_col].values
        min_error = float('inf')
        best_match = None

        for ideal_col in ideal_data.columns:
            if ideal_col == 'x':
                continue

            # Only compare rows where x matches
            ideal_y = ideal_data.loc[ideal_data['x'].isin(train_x), ideal_col].values
            error = np.sum((train_y - ideal_y) ** 2)

            if error < min_error:
                min_error = error
                best_match = ideal_col

        best_matches[train_col] = best_match

        # Calculate max deviation for this best match
        best_ideal_y = ideal_data.loc[ideal_data['x'].isin(train_x), best_match].values
        max_dev = np.max(np.abs(train_y - best_ideal_y))
        max_deviations[train_col] = max_dev

    return best_matches, max_deviations

best_matches, max_deviations = find_best_ideal_functions(training_data, ideal_data)

# %%
# -------------------------------------------------------------------------------------
# Function: Map Test Points to Ideal
# --------------------------------------------------------------------------------------

def map_test_points_to_ideal(test_data, ideal_data, best_matches, max_deviations):
    """
    Maps each test data point to its closest matching ideal function (within threshold).

    Args:
        test_data (pd.DataFrame): DataFrame with x and y from the test dataset.
        ideal_data (pd.DataFrame): DataFrame with ideal function values for all x.
        best_matches (dict): Mapping of training function -> best ideal match.
        max_deviations (dict): Max deviation thresholds per matched ideal function.

    returns:
        list: each dict contains info about a matched test point (x, y, train_function, ideal_function, deviation, threshold).
    """
    mapped_points = []

    for index, row in test_data.iterrows():
        x_val = row['x']
        y_val = row['y']
        best_fit = None
        smallest_deviation = float('inf')

        for train_col, ideal_col in best_matches.items():
            # get the corresponding ideal_y value for this x
            ideal_row = ideal_data[ideal_data['x'] == x_val]

            if not ideal_row.empty:
                ideal_y = ideal_row[ideal_col].values[0]
                deviation = abs(y_val - ideal_y)
                threshold = max_deviations[train_col] * np.sqrt(2)

                if deviation <= threshold and deviation < smallest_deviation:
                    best_fit = {
                        'x': x_val,
                        'y': y_val,
                        'train_function': train_col,
                        'ideal_function': ideal_col,
                        'deviation': deviation,
                        'threshold': threshold
                    }
                    smallest_deviation = deviation

        if best_fit:
            mapped_points.append(best_fit)
    
    return mapped_points

mapped_points = map_test_points_to_ideal(test_data, ideal_data, best_matches, max_deviations)

mapped_df = pd.DataFrame(mapped_points).reset_index(drop=True)

# print(mapped_df)

# --------------------------------------------------------------
# Save mapped test data to database
# --------------------------------------------------------------
save_best_fit(mapped_points, engine=results_engine)

# --------------------------------------------------------------
# Visualization of results
# --------------------------------------------------------------

# plot best-fitting ideal functions for each training function
plot_best_matches(training_data, ideal_data, best_matches)


# Add column for visualization
mapped_df['matched_function'] = mapped_df['ideal_function']

# plot test points against their matched ideal functions
plot_test_vs_ideal(mapped_df, ideal_data)


# plot deviations between test points and ideal functions
plot_deviations(mapped_df)

# %%
