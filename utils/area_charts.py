import streamlit as st
import pandas as pd
import os

from utils.config import UPLOAD_FOLDER

def generate_charts_for_area(area):
    """Generate charts based on the data for the given area."""
    area_path = os.path.join(UPLOAD_FOLDER, area)
    
    latest_file = max(os.listdir(area_path), key=lambda x: os.path.getmtime(os.path.join(area_path, x)))
    filepath = os.path.join(area_path, latest_file)

    try:
        if latest_file.endswith(".csv"):
            data = pd.read_csv(filepath)
        elif latest_file.endswith(".xlsx"):
            data = pd.read_excel(filepath)
        elif latest_file.endswith(".json"):
            data = pd.read_json(filepath)
        else:
            st.error("Unsupported file format.")
            return

        # Customize charts per area as needed
        st.write(data.head())  # Display data preview
        st.line_chart(data.select_dtypes(include=["number"]))

    except Exception as e:
        st.error(f"Error reading file {latest_file}: {e}")
