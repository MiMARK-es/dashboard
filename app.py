import streamlit as st
from components.layout import setup_page, setup_tabs
from components.upload_section import display_upload_section
from components.dashboard_section import display_dashboard
from utils.config import areas

# Initialize page layout and load CSS
setup_page()

# Create tabs for Uploads and Dashboard
tab_uploads, tab_dashboard = setup_tabs(["Upload Files", "General Dashboard"])

# Display Upload Section in tab_uploads
with tab_uploads:
    display_upload_section(areas)

# Display Dashboard Section in tab_dashboard
with tab_dashboard:
    display_dashboard(areas)
