import streamlit as st
from utils.file_utils import handle_upload, validate_file_format
from utils.config import AREAS

def display_upload_section():
    """Display file upload sections based on the areas configuration."""
    col_left, col_right = st.columns(2)

    for i, (area, files_config) in enumerate(AREAS.items()):
        col = col_left if i % 2 == 0 else col_right
        with col:
            st.subheader(f"{area}")
            for expected_file, expected_columns in files_config.items():
                uploaded_file = st.file_uploader(f"Upload {expected_file} file (CSV or XLSX):", type=["csv", "xlsx"], key=f"{area}_{expected_file}")
                if uploaded_file:
                    if validate_file_format(uploaded_file, expected_file, area):
                        handle_upload(uploaded_file, area, expected_file)
                        st.success(f"File '{uploaded_file.name}' uploaded for {area}.")
                    else:
                        st.error(f"File '{uploaded_file.name}' does not match the expected format for '{expected_file}'.")
