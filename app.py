import streamlit as st
from utils.file_utils import handle_upload, get_last_upload_info, is_valid_format
from utils.area_charts import generate_charts_for_area
import os

# Define the six areas
areas = ['clinica', 'financial', 'technical', 'hr', 'regulatory', 'business']
UPLOAD_FOLDER = '/var/data/uploads'

# Create two main tabs
tab_uploads, tab_dashboard = st.tabs(["Upload Files", "General Dashboard"])

# File upload tab
with tab_uploads:
    st.header("Upload Data Files")
    for area in areas:
        st.subheader(f"{area.capitalize()}")
        uploaded_file = st.file_uploader(f"Upload a file for {area}", type=["csv", "xlsx", "json"], key=area)
        if uploaded_file:
            handle_upload(uploaded_file, area, UPLOAD_FOLDER)
            st.success(f"File uploaded for {area}.")

# General dashboard tab
with tab_dashboard:
    st.header("General Dashboard")
    cols = st.columns(3)  # Create columns for side-by-side chart display (2 rows, 3 columns)

    for i, area in enumerate(areas):
        col = cols[i % 3]  # Distribute areas across the columns
        with col:
            st.subheader(f"{area.capitalize()}")
            last_upload_info = get_last_upload_info(area, UPLOAD_FOLDER)
            if last_upload_info:
                st.caption(f"Last upload: {last_upload_info['timestamp']} (File: {last_upload_info['filename']})")
                generate_charts_for_area(area, UPLOAD_FOLDER)
            else:
                st.warning(f"No data available for {area} yet.")
