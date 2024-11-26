import streamlit as st
from components.layout import setup_page, setup_tabs
from components.upload_section import display_upload_section
from components.dashboard_section import display_dashboard
from components.area_sections import *
from utils.file_utils import all_files_present
from utils.config import AREAS

# Initialize page layout and load CSS
setup_page()

tab_names = ["Upload Files", "General Dashboard"]

# Add tabs for each area that has all files present
tab_index = 2
sections_tabs = {}
for area in AREAS:
    if all_files_present(area):
        tab_names.append(area)
        sections_tabs[area] = tab_index
        tab_index += 1

# Create tabs for Uploads, Dashboard and each included area
tabs = setup_tabs(tab_names)

# Display Upload Section in tab_uploads
with tabs[0]:
    display_upload_section()

# Display Dashboard Section in tab_dashboard
with tabs[1]:
    display_dashboard()

for i in range(2, len(tabs)):
    with tabs[i]:
        area = tab_names[i]
        globals()[f"display_{area.lower()}"]()


