import streamlit as st
from utils.file_utils import get_last_upload_info, all_files_present
from utils.area_charts import generate_charts_for_area
from utils.config import UPLOAD_FOLDER, AREAS
import os

def display_dashboard():
    """Display a dashboard for each area with last upload info and a dummy plot."""
    cols = st.columns(3)

    for i, (area, expected_files) in enumerate(AREAS.items()):
        col = cols[i % 3]
        with col:
            st.subheader(f"{area}")
            
            for expected_file in expected_files:
                last_upload_info = get_last_upload_info(area, expected_file)
                if not last_upload_info:
                    st.warning(f"No data available for '{expected_file}' in {area} yet.")
                    # st.caption(f"Last upload for '{expected_file}': {last_upload_info['timestamp']} (File: {last_upload_info['filename']})")

            if all_files_present(area):
                generate_charts_for_area(area)
