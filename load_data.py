"""
load_data.py

Author: Patrick Beal

Creates SQLite db and loads CSV data into the db
"""

import os

import pandas as pd
import sqlite3

def init_db(db_path="cell-count.db", schema_path="schema.sql"):
    conn = sqlite3.connect(db_path)

    # Read and execute the schema to set up the database
    with open(schema_path, 'r') as f:
        schema = f.read()

    try:
        conn.executescript(schema)
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occured during db init: {e}")
    finally:
        conn.close()

def load_data(db_path="cell-count.db", data_path="cell-count.csv"):
    # Initialize database if not done
    if os.path.exists(db_path):
        os.remove(db_path)
    init_db(db_path)

    conn = sqlite3.connect(db_path)

    # Load data, split into subjects and samples, and save to db
    cell_data = pd.read_csv(data_path).rename(columns={"subject": "subject_id", "sample": "sample_id"})

    subjects = cell_data[cell_data.columns[:7]].drop_duplicates()

    samples = cell_data[['subject_id'] + list(cell_data.columns[7:])]

    # making sure there are 3 samples / subject
    assert subjects.shape[0] == samples.shape[0] / 3 

    # Write the two tables to databases
    subjects.to_sql("subjects", con=conn, if_exists='append', index=False)
    samples.to_sql("samples", con=conn, if_exists='append', index=False)

if __name__ == "__main__":
    load_data()
