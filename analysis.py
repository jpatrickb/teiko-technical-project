"""
analysis.py

Author: Patrick Beal

Uses data from the SQLite DB to run analyses
"""

import os 

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import sqlite3

from scipy import stats
from statsmodels.stats.multitest import multipletests

def initial_analysis(db_path="cell-count.db"):
    if not os.path.exists(db_path):
        from load_data import load_data
        load_data()

    conn = sqlite3.connect(db_path)

    # Load the data into a dataframe
    samples = pd.read_sql_query("SELECT * FROM samples", conn)

    conn.commit()
    conn.close()

    # Calculate total
    samples['total_count'] = samples['b_cell'] + samples['cd8_t_cell'] + samples['cd4_t_cell'] + samples['nk_cell'] + samples['monocyte']

    # Convert to long
    samples_long = pd.melt(
        samples,
        id_vars=['sample_id', 'total_count'],
        value_vars=['b_cell', 'cd8_t_cell', 'cd4_t_cell', 'nk_cell', 'monocyte'],
        var_name='population',
        value_name='count'
    )
    # Calculate percentage for each population
    samples_long['percentage'] = 100 * samples_long['count'] / samples_long['total_count']

    # Rename to `sample` for correctness
    samples_long = samples_long.rename(columns={"sample_id": "sample"})
    return samples_long


def statistical_analysis(db_path="cell-count.db", img_path="images/cells-by-response.png"):
    summary_df = initial_analysis(db_path)

    conn = sqlite3.connect(db_path)

    # Load the subjects
    subjects = pd.read_sql_query(
"""
SELECT s.sample_id AS sample, sub.subject_id, sub.response, s.sample_type
FROM samples s
JOIN subjects sub ON s.subject_id = sub.subject_id
WHERE sub.condition = 'melanoma' 
  AND sub.treatment = 'miraclib' 
  AND s.sample_type = 'PBMC'
""",
    con=conn
    )

    # Merge subjects with our summary dataframe
    merged_df = pd.merge(
        subjects,
        summary_df,
        on="sample"
    )

    # Boxplot by population type
    populations = merged_df['population'].unique()
    pop_t_vals = {}
    for i in range(5):
        # Get df with only the desired population
        pop_df = merged_df[merged_df['population'] == populations[i]]

        # Do a t-test and save the stat
        responders = pop_df[pop_df['response'] == 'yes']['percentage']
        non_responders = pop_df[pop_df['response'] == 'no']['percentage']

        pop_t_vals[populations[i]] = stats.ttest_ind(responders, non_responders, equal_var=False)

        # Plot the boxplot
        plt.subplot(2, 3, i + 1)
        plt.title(populations[i])
        sns.boxplot(data=pop_df, x='response', y='percentage')

    # Saves the image
    plt.tight_layout()
    plt.suptitle("Difference in Cell Percents by Response")
    plt.subplots_adjust(top=0.88) # manually tuned to make the title fit
    plt.savefig(img_path, dpi=300)

    # Multiple test correction before returning
    raw_p_values = [pop_t_vals[p].pvalue for p in populations]
    reject, adjusted_p_vals , _, _ = multipletests(raw_p_values, alpha=0.05, method='fdr_bh')

    results = {}
    for i, p in enumerate(populations):
        results[p] = {
            't_stat': pop_t_vals[p].statistic,
            'p_raw': raw_p_values[i],
            'p_adj': adjusted_p_vals[i],
            'significant': reject[i]
        }

    return pd.DataFrame(results), img_path, merged_df


def baseline_cohort(db_path="cell-count.db"):
    conn = sqlite3.connect(db_path)

    # Load the subjects
    baseline = pd.read_sql_query(
"""
SELECT s.sample_id AS sample, sub.project, sub.subject_id, sub.response, s.sample_type, sub.sex
FROM samples s
JOIN subjects sub ON s.subject_id = sub.subject_id
WHERE sub.condition = 'melanoma' 
  AND s.time_from_treatment_start = 0
  AND s.sample_type = 'PBMC'
  AND sub.treatment = 'miraclib'
""",
    con=conn
    )
    conn.close()

    samples_by_project = pd.pivot_table(
        data=baseline, 
        values='sample', 
        index='project', 
        aggfunc='count'
    )
    subjects_by_response = pd.pivot_table(
        data=baseline, 
        values='subject_id', 
        index='response', 
        aggfunc='count'
    )
    subjects_by_sex = pd.pivot_table(
        data=baseline,
        values='subject_id',
        index='sex',
        aggfunc='count'
    )
    return samples_by_project, subjects_by_response, subjects_by_sex


def b_cell_calculation(db_path="cell-count.db"):
    conn = sqlite3.connect(db_path)
    
    # Load the subjects
    result = pd.read_sql_query(
"""
SELECT AVG(s.b_cell) AS avg_b_cell
FROM samples s
JOIN subjects sub ON s.subject_id = sub.subject_id
WHERE sub.condition = 'melanoma' 
  AND sub.sex = 'M'
  AND sub.response = 'yes'
  AND s.time_from_treatment_start = 0
""",
    con=conn
    )
    conn.close()

    avg_b_cell = result['avg_b_cell'].iloc[0]
    return avg_b_cell

if __name__ == "__main__":
    print(baseline_cohort())
    print(f"{b_cell_calculation():.2f}")