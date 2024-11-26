import streamlit as st
from utils.config import UPLOAD_FOLDER
from utils.file_utils import load_data
from utils.data_utils import display_dataframes
import altair as alt

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

        # Create a horizontal bar chart with Altair
        chart = alt.Chart(center_data).mark_bar(color="skyblue").encode(
            y=alt.Y("Seleccione su Hospital:N", title="", sort='-x'),  # Hospital names on y-axis
            x=alt.X("Sample Count:Q", title="Number of Samples")  # Sample count on x-axis
        ).properties(
            width=700,  # Chart width
            height=400 + len(center_data) * 15  # Adjust height dynamically based on number of hospitals
        ).configure_axis(
            labelFontSize=12,  # Increase font size for readability
            labelLimit=0  # Ensure full labels are displayed (no trimming)
        ).configure_view(
            strokeWidth=0  # Remove the border around the chart for cleaner appearance
        )

        # Display the chart
        st.altair_chart(chart, use_container_width=True)

    with col3:
        st.write("### Samples per Condition")

        pathology_data = df_redcap.groupby("Patología").size().reset_index(name="Sample Count")

        chart = alt.Chart(pathology_data).mark_bar(color="salmon").encode(
            y=alt.Y("Patología:N", title="", sort='-x'),
            x=alt.X("Sample Count:Q", title="Number of Samples")
        ).properties(
            width=700,
            height=400 + len(pathology_data) * 15
        ).configure_axis(
            labelFontSize=12,
            labelLimit=0
        ).configure_view(
            strokeWidth=0
        )

        st.altair_chart(chart, use_container_width=True)
