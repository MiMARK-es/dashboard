import streamlit as st
from utils.config import UPLOAD_FOLDER
from utils.file_utils import load_data
from utils.data_utils import display_dataframes
import plotly.graph_objects as go

def display_clinical():
    # Load data from the uploaded files
    clinical_data = load_data("Clinical")
    df_redcap = clinical_data["RedCap"]
    df_benchling = clinical_data["Benchling"]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("### Uploaded Data")
        display_dataframes(clinical_data)

    with col2:
        st.write("### Samples per Center")

        # Group by center
        center_data = df_redcap.groupby("Seleccione su Hospital").size().reset_index(name="Sample Count")
        center_data = center_data.sort_values("Sample Count", ascending=True)  # Sort for better visualization

        # Create a horizontal bar chart with Plotly
        fig_center = go.Figure(
            go.Bar(
                x=center_data["Sample Count"],
                y=center_data["Seleccione su Hospital"],
                orientation="h",  # Horizontal bars
                marker=dict(color="skyblue"),
                name="Samples per Center"
            )
        )

        # Customize layout
        fig_center.update_layout(
            xaxis=dict(title="Number of Samples"),
            yaxis=dict(title="", automargin=True),  # Ensure hospital names are fully visible
            height=400 + len(center_data) * 20,  # Dynamically adjust height based on data size
            title="Samples per Center",
            showlegend=False,
            dragmode="pan",
        )

        # Display the chart
        st.plotly_chart(fig_center, use_container_width=True)

    with col3:
        st.write("### Samples per Condition")

        # Group by condition
        pathology_data = df_redcap.groupby("Patología").size().reset_index(name="Sample Count")
        pathology_data = pathology_data.sort_values("Sample Count", ascending=True)

        # Create a horizontal bar chart with Plotly
        fig_condition = go.Figure(
            go.Bar(
                x=pathology_data["Sample Count"],
                y=pathology_data["Patología"],
                orientation="h",  # Horizontal bars
                marker=dict(color="salmon"),
                name="Samples per Condition"
            )
        )

        # Customize layout
        fig_condition.update_layout(
            xaxis=dict(title="Number of Samples"),
            yaxis=dict(title="", automargin=True),  # Ensure condition names are fully visible
            height=400 + len(pathology_data) * 20,  # Dynamically adjust height based on data size
            title="Samples per Condition",
            showlegend=False,
            dragmode="pan",
        )

        # Display the chart
        st.plotly_chart(fig_condition, use_container_width=True)
