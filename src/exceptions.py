#%%
"""
exceptions.py

Defines custom exception classes for the project.
"""


class DataLoadError(Exception):
    """
    Exception raises for errors encountered during data loading operations.

    This exception should be raised when a data file cannot be loaded,
    e.g: due to a missing file, incorrect format, or read error.
    """
    pass 