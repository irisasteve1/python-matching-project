# %%
"""
cleanup_db.py

Utility script to clean up specific tables from the results and functions databases.
Used during development/testing to reset the state of the SQLite databases.
"""

from sqlalchemy import create_engine, inspect

def drop_tables(db_path, tables_to_drop):
    """
    Drops specified tables from a given SQLite database.

    Args:
        db_path (str): Path to the SQLite database file.
        table_to_drop (list): List of table names to drop.

    Returns:
        None
    """
    engine = create_engine(f"sqlite:///{db_path}")
    inspector = inspect(engine)

    with engine.connect() as conn:
        for table in tables_to_drop:
            if table in inspector.get_table_names():
                conn.execute(f'DROP TABLE IF EXISTS {table}')
                print(f"Dropped {table} from {db_path}")
            else:
                print(f"{table} not found in {db_path}")


# clean up results.db
drop_tables("database/results.db", [
    "ideal_functions",
    "test_functions",
    "train_functions"
])

# clean up functions.db
drop_tables("database/functions.db", [
    "best_fit_points"
])
