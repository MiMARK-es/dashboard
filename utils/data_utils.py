import streamlit as st
import pandas as pd

def display_dataframes(data):
    """Display the dataframes for the given area."""
    for df_name, df in data.items():
        st.markdown(f"#### {df_name}")
        st.write(df)