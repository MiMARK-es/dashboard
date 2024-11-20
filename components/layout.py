import streamlit as st

def setup_page():
    """Sets up the page layout and loads custom CSS."""
    st.set_page_config(layout="wide", page_title="MiMARK Dashboard")
    with open("assets/styles.css") as css_file:
        st.markdown(f'<style>{css_file.read()}</style>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 5])
    with col1:
        st.image("assets/logo.jpg", width=300, use_container_width=False)
    with col2:
        st.header("Dashboard")

def setup_tabs(tab_names):
    """Creates tabs for different sections of the app."""
    return st.tabs(tab_names)
