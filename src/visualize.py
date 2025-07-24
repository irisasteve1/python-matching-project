# %%

"""
Visualize.py

This module provides visualization functions for:
1. Plotting best matches between training and ideal functions.
2. Plotting test data points against their matched ideal functions.
3. Plotting deviation of test points from the matched ideal function with thresholds.

"""
# --------------------------------------------------------------
# third-party imports
# --------------------------------------------------------------

import os
import matplotlib.pyplot as plt

# Create plots folder for saved visuals
PLOT_DIR = "plots"
os.makedirs(PLOT_DIR, exist_ok=True)

# --------------------------------------------------------------
# Plot best matches between training data and ideal data
# --------------------------------------------------------------

def plot_best_matches(training_data, ideal_data, best_matches):
    """
    Plot the best-matching ideal functions for each training function.

    Parameters:
    - training_data (pd.DataFrame): Dataframe containing the training dataset.
    - ideal_data (pd.DataFrame): Dataframe containing the ideal functions.
    - best_matches (dict): Dictionary mapping training functions to their best-matching ideal functions.

    returns:
    - None
    """
    for train_col, ideal_col in best_matches.items():
        train_x = training_data['x']
        train_y = training_data[train_col]
        ideal_y = ideal_data[ideal_col][ideal_data['x'].isin(train_x)]

        plt.figure(figsize=(8, 4))
        plt.plot(train_x, train_y, label=f"Train {train_col}", marker='o', markersize=6, linewidth=2)
        plt.plot(train_x, ideal_y.values, label=f"Ideal {ideal_col}", linestyle='--', linewidth=2, color='red')
        plt.fill_between(train_x, train_y, ideal_y.values, color='gray', alpha=0.2, label='Difference')
        plt.title(f"Match: {train_col} → {ideal_col}")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(PLOT_DIR, f"{train_col}_vs_{ideal_col}.png"))
        plt.close()


# --------------------------------------------------------------
# Plot best matches between test data and ideal data
# --------------------------------------------------------------

def plot_test_vs_ideal(test_data, ideal_data):
    """
    Plot test points alongside their matched ideal functions.

    parameters:
    - test_data: Dataframe containing test points with matched ideal functions.
    - ideal_data: Dataframe containing the ideal functions.

    Returns:
    - None
    """
    for func in test_data['matched_function'].unique():
        subset = test_data[test_data['matched_function'] == func]
        ideal_subset = ideal_data[['x', func]]

        plt.figure(figsize=(8, 4))
        plt.plot(ideal_subset['x'], ideal_subset[func], label=f'Ideal: {func}', color='green')
        plt.scatter(subset['x'], subset['y'], color='orange', label='Test Points')

        plt.title(f"Test vs Ideal Match: {func}")
        plt.xlabel('x')
        plt.ylabel('y')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(PLOT_DIR, f"test_vs_{func}.png"))
        plt.close()


# ----------------------------------------------------------------
# Plot deviation of test points from their matched ideal function
# ----------------------------------------------------------------

def plot_deviations(test_data):
    """
    Plot deviations between test points and their matched ideal function values.

    Parameters:
    - test_data: Dataframe containing test points with actual and ideal values.

    Returns:
    - None
    """
    for func in test_data['matched_function'].dropna().unique():
        subset = test_data[test_data['matched_function'] == func]

        subset = subset.sort_values(by='x')
        deviations = subset['deviation']
        threshold = subset['threshold'].iloc[0]

        plt.figure(figsize=(8,4))
        plt.bar(subset['x'], deviations, color='skyblue', label='Deviation')
        plt.axhline(y=threshold, color='red', linestyle='--', label='Threshold')

        plt.title(f'Deviations from Ideal Function: {func}')
        plt.xlabel('x')
        plt.ylabel('|y_test - y_ideal|')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(PLOT_DIR, f"deviations_{func}.png"))
        plt.close()
