"""
dashboard.py

Author: Patrick Beal

Runs the interactive streamlit dashboard showing the analysis results
"""

import os

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Teiko Cell Count Analysis Project", layout="wide")
st.title("Teiko Cell Count Analysis Project")

tab2, tab3, tab4 = st.tabs([
    "Part 2: Initial Analysis",
    "Part 3: Statistical Analysis",
    "Part 4: Data Subset Analysis"
])

with tab2:
    st.header("Relative Frequences by Sample")
    st.dataframe(pd.read_csv("outputs/part2_frequencies.csv"), width="content")

with tab3:
    st.header("Responders vs Non-Responders with melanoma, miraclib, PBMC")
    stats_df = pd.read_csv("outputs/part3_stats.csv")

    st.markdown("The results of the analysis, including with Benjamini-Hochberg $p$-value correction:")
    st.dataframe(stats_df, width="content")

    st.markdown("Based on these results, with the $p$-value correction, only the `cd4_t_cells` have a statistically significant difference in relative frequencies between responders and non-responders.")

    st.markdown("The box plots compare the relative frequencies between responders and non-responders across all cell populations.")
    st.image("outputs/cells-by-response.png")

with tab4:
    st.header("Baseline Cohort")

    

    st.markdown("Number of Samples per Project")
    st.dataframe(pd.read_csv("outputs/part4_by_project.csv"), width="content")

    st.markdown("Number of Responders/Non-Responders")
    st.dataframe(pd.read_csv("outputs/part4_by_response.csv"), width="content")

    st.markdown("Number of Men/Women")
    st.dataframe(pd.read_csv("outputs/part4_by_sex.csv"), width="content")

    with open("outputs/part4_b_cell_avg.txt") as f:
        avg_b_cell = f.read().strip()
    st.metric("Avg B cells for melanoma males/responders/on day 0 of treatment", avg_b_cell)