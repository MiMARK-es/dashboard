import streamlit as st
from utils.file_utils import get_last_upload_info
from utils.area_charts import generate_charts_for_area
import os

from utils.config import UPLOAD_FOLDER


def display_dashboard(areas):
    """Display a dashboard for each area with last upload info and a dummy plot."""
    cols = st.columns(3)

    for i, (area, expected_files) in enumerate(areas.items()):
        col = cols[i % 3]
        with col:
            st.subheader(f"{area}")
            all_files_present = all(
                any(
                    os.path.exists(os.path.join(UPLOAD_FOLDER, area, f"{area}_{file}.{ext}"))
                    for ext in ["csv", "xlsx"]
                )
                for file in expected_files
            )
            for expected_file in expected_files:
                last_upload_info = get_last_upload_info(area, expected_file)
                if last_upload_info:
                    st.caption(f"Last upload for '{expected_file}': {last_upload_info['timestamp']} (File: {last_upload_info['filename']})")
                    file_path = os.path.join(UPLOAD_FOLDER, area, last_upload_info['filename'])
                    if os.path.exists(file_path):
                        st.markdown(f"[View {expected_file} Data](/{file_path})", unsafe_allow_html=True)
                else:
                    st.warning(f"No data available for '{expected_file}' in {area} yet.")

            if all_files_present:
                generate_charts_for_area(area)
