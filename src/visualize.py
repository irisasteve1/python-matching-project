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
from turtle import color
import matplotlib.pyplot as plt
from numpy import size

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

from bokeh.plotting import figure, show, output_file, save
from bokeh.io import output_notebook
from bokeh.layouts import column
from bokeh.palettes import Category10
import os

def plot_test_vs_ideal_bokeh(test_data, ideal_data, output_dir="plots/bokeh"):
    """
    Interactive Bokeh plot: test points vs. ideal function.

    Parameters:
    - test_data (pd.DataFrame): must have 'x', 'y', 'matched_function'
    - ideal_data (pd.DataFrame): must have 'x' and ideal functions
    output_dir (str): folder to save HTML files

    Returns:
    - None
    """
    os.makedirs(output_dir, exist_ok=True)
    plots = []

    for i, func in enumerate(test_data['matched_function'].unique()):
        subset = test_data[test_data['matched_function'] == func]
        ideal_subset = ideal_data[['x', func]]

        p = figure(title=f"Test vs Ideal Function: {func}", x_axis_label='x', y_axis_label='y', width=700, height=400)
        color = Category10[10][i % 10]

        # plot ideal function
        p.line(ideal_subset['x'], ideal_subset[func],
        legend_label=f"Ideal: {func}", color=color, line_width=2)

        # plot test points
        p.circle(subset['x'], subset['y'],
        size=8, color='orange', legend_label='Test Points')

        p.legend.location = "top_left"
        p.grid.visible = True
        plots.append(p)

        # save individual plots
        save(p, filename=os.path.join(output_dir, f"test_vs_{func}.html"))