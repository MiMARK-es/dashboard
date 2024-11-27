import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from streamlit_plotly_events import plotly_events
from utils.file_utils import load_data

def display_clinical():
    """Display clinical data with interactive and responsive charts."""
    # Load data from the uploaded files
    clinical_data = load_data("Clinical")
    df_redcap = clinical_data["RedCap"]
    df_benchling = clinical_data["Benchling"]

    # Initialize session state for filtering
    if "selected_center" not in st.session_state:
        st.session_state["selected_center"] = None
    if "selected_condition" not in st.session_state:
        st.session_state["selected_condition"] = None

    # Filter data based on session state
    filtered_data = df_redcap.copy()
    if st.session_state["selected_center"]:
        filtered_data = filtered_data[filtered_data["Seleccione su Hospital"] == st.session_state["selected_center"]]
    if st.session_state["selected_condition"]:
        filtered_data = filtered_data[filtered_data["Patología"] == st.session_state["selected_condition"]]

    # Display active filters as pills
    st.write("### Filters")
    active_filters = []
    if st.session_state["selected_center"]:
        active_filters.append(f"Center: {st.session_state['selected_center']}")
    if st.session_state["selected_condition"]:
        active_filters.append(f"Condition: {st.session_state['selected_condition']}")

    if active_filters:
        st.info(" | ".join(active_filters))
    else:
        st.info("By clicking on a specific center or condition in the charts below, you can filter the data!")

    # Reset filters button
    if st.button("Reset Filters"):
        st.session_state["selected_center"] = None
        st.session_state["selected_condition"] = None
        st.rerun()  # Trigger a rerun

    # Create three columns
    col1, col2, col3 = st.columns(3)

    # Column 1: Dataframes
    with col1:
        st.write("### Uploaded Data")
        st.write("#### RedCap Data")
        st.dataframe(df_redcap)
        st.write("#### Benchling Data")
        st.dataframe(df_benchling)

    # Column 2: Samples per Center
    with col2:
        st.write("### Samples per Center")

        # Group by center
        center_data = filtered_data.groupby("Seleccione su Hospital").size().reset_index(name="Sample Count")
        center_data = center_data.sort_values("Sample Count", ascending=False)

        # Create a horizontal bar chart for centers
        fig_center = go.Figure(
            go.Bar(
                x=center_data["Sample Count"],
                y=center_data["Seleccione su Hospital"],
                orientation="h",
                marker=dict(color="skyblue"),
                name="Samples per Center",
            )
        )

        # Customize layout
        fig_center.update_layout(
            xaxis=dict(title="Number of Samples"),
            yaxis=dict(title="", automargin=True),
            title="Samples per Center",
            showlegend=False,
            dragmode="pan",
            autosize=True, 
        )

        # Display the chart and capture click events
        center_click = plotly_events(
            fig_center,
            click_event=True,
            select_event=False,
            # override_height based on the number of centers
            override_height= 200 + 20*len(center_data) if len(center_data) > 10 else 200
        )

        if center_click and len(center_click) > 0:
            selected_center = center_click[0].get("y", None)  # Safely extract "y"
            if selected_center and selected_center != st.session_state["selected_center"]:
                st.session_state["selected_center"] = selected_center
                st.rerun()  # Trigger a rerun

    # Column 3: Samples per Condition
    with col3:
        st.write("### Samples per Condition")

        # Group by condition
        pathology_data = filtered_data.groupby("Patología").size().reset_index(name="Sample Count")
        pathology_data = pathology_data.sort_values("Sample Count", ascending=False)

        # Create a horizontal bar chart for conditions
        fig_condition = go.Figure(
            go.Bar(
                x=pathology_data["Sample Count"],
                y=pathology_data["Patología"],
                orientation="h",
                marker=dict(color="salmon"),
                name="Samples per Condition"
            )
        )

        # Customize layout
        fig_condition.update_layout(
            xaxis=dict(title="Number of Samples"),
            yaxis=dict(title="", automargin=True),
            title="Samples per Condition",
            showlegend=False,
            dragmode="pan",
            autosize=True, 
        )

        # Display the chart and capture click events
        condition_click = plotly_events(
            fig_condition,
            click_event=True,
            select_event=False,
            override_height=400
        )
        if condition_click and len(condition_click) > 0:
            selected_condition = condition_click[0].get("y", None)  # Safely extract "y"
            if selected_condition and selected_condition != st.session_state["selected_condition"]:
                st.session_state["selected_condition"] = selected_condition
                st.rerun()  # Trigger a rerun
