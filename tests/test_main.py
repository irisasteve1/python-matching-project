# %%
"""
test_main.py

Unit tests for the main analysis functions in main.py, including:
- find_best_ideal_functions: Checks best ideal function matching and deviation calculation
- map_test_points_to_ideal: Checks correct mapping of test points to ideal functions
"""
import pandas as pd
import sys
import os

# Add the path to main.py (adjust this if your structure is different)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import find_best_ideal_functions

from pathlib import Path


def test_find_best_ideal_functions_returns_correct_matches():
    
    """
    Unit test for find_best_ideal_functions in main.py.

    Verifies:
    - The best ideal function for each training column is correctly identified using least squares.
    - The returned max_deviations dictionary contains float values.

    Raises:
        AssertionError: if the best match or deviation type is incorrect.
    """
    # create dummy training data
    training_data = pd.DataFrame({
        'x': [1,2,3],
        'y1': [2,4,6],
        'y2': [3,6,9]
    })

    # create ideal data with slight noise
    ideal_data = pd.DataFrame({
        'x': [1,2,3],
        'y41': [2.1, 4.1, 6.1] ,   # close to y1
        'y42': [3.05, 6.05, 9.05] # close to y2
    })

    # run function
    best_matches, max_devs = find_best_ideal_functions(training_data, ideal_data)

    # check best_matches mapping
    assert best_matches['y1'] == 'y41'
    assert best_matches['y2'] == 'y42'

    # check deviations are returned and are float numbers
    assert isinstance(max_devs['y1'], float)
    assert isinstance(max_devs['y2'], float)

    # print for debugging 
    print("Best Matches:", best_matches)
    print("Max deviations:", max_devs)


def test_map_test_points_to_ideal_returns_expected_mapping():
    """
    Unit test for map_test_points_to_ideal in main.py.

    This test verifies that:
    - A test point within the deviation threshold is mapped to the correct ideal function.
    - The mapping result contains expected keys and values.

    Raises:
        AssertionError: If the mapping is incorrect or missing expected keys/values.
    """
    from main import map_test_points_to_ideal

    # setup
    test_data = pd.DataFrame({'x': [2], 'y': [4.05]})
    ideal_data = pd.DataFrame({
        'x': [1,2,3],
        'y41': [2.1, 4.1, 6.1]
    })
    best_matches = {'y1': 'y41'}
    max_devs = {'y1': 0.1}

    # run mapping function
    results = map_test_points_to_ideal(test_data, ideal_data, best_matches, max_devs)

    print("Returned results:", results)

    # check results
    assert len(results) == 1
    assert abs(results[0]['deviation'] - 0.05) < 1e-6
    assert results[0]['ideal_function'] == 'y41'
    assert results[0]['train_function'] == 'y1'