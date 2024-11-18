import streamlit as st
import os
import shutil
import pandas as pd
from datetime import datetime

# Custom module for utility functions
from utils.file_utils import is_valid_format

# Create directories if not already present
os.makedirs("uploads", exist_ok=True)
os.makedirs("backups", exist_ok=True)

# Streamlit app with two tabs
st.set_page_config(page_title="File Dashboard", layout="wide")

tab1, tab2 = st.tabs(["File Uploads", "Dashboard"])

with tab1:
    st.header("Upload Data Files")
    uploaded_file = st.file_uploader("Upload a file", type=["csv", "xlsx", "json"])

    if uploaded_file:
        # Validate file format
        if is_valid_format(uploaded_file, [".csv", ".xlsx", ".json"]):
            # Save uploaded file to 'uploads' directory
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filepath = os.path.join("uploads", uploaded_file.name)

            # Back up old file if it exists
            if os.path.exists(filepath):
                backup_path = os.path.join("backups", f"{uploaded_file.name}_{timestamp}")
                shutil.move(filepath, backup_path)

            # Save new file
            with open(filepath, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success("File uploaded and saved successfully!")
        else:
            st.error("Invalid file format. Please upload a CSV, XLSX, or JSON.")

with tab2:
    st.header("Dashboard")
    if os.listdir("uploads"):
        latest_files = {}
        for file in os.listdir("uploads"):
            area = file.split('_')[0]  # Assume filenames start with area (e.g., 'clinics_data.csv')
            if area not in latest_files or os.path.getmtime(os.path.join("uploads", file)) > os.path.getmtime(os.path.join("uploads", latest_files[area])):
                latest_files[area] = file

        for area, file in latest_files.items():
            st.subheader(f"Latest Data for {area.capitalize()}")
            filepath = os.path.join("uploads", file)
            try:
                if file.endswith(".csv"):
                    data = pd.read_csv(filepath)
                elif file.endswith(".xlsx"):
                    data = pd.read_excel(filepath)
                elif file.endswith(".json"):
                    data = pd.read_json(filepath)
                else:
                    continue

                # Display preview and chart
                st.write(data.head())
                st.line_chart(data.select_dtypes(include=["number"]))
            except Exception as e:
                st.error(f"Error reading file {file}: {e}")
    else:
        st.warning("No files uploaded yet.")
