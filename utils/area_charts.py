import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import altair as alt
from utils.file_utils import load_data


from utils.config import UPLOAD_FOLDER, AREAS

def generate_charts_for_area(area):
    """Generate charts based on the data for the given area."""
    if area not in AREAS:
        st.error(f"Area '{area}' not found.")
        return

    # For each area, redirect to the function that generates the specific charts
    # using the area name to compose the function name as generate_{area}_main_chart
    generate_function = globals().get(f"generate_{area.lower()}_main_chart")
    if generate_function:
        generate_function()
    else:
        st.error(f"No chart generation function found for area '{area}'.")


def generate_clinical_main_chart():
    """Generate main chart for the Clinical area."""
    # Load data from the uploaded files
    clinical_data = load_data("Clinical")
    
    df_redcap = clinical_data["RedCap"]
    df_benchling = clinical_data["Benchling"]

    # Drop blank Fecha rows
    df_redcap = df_redcap.dropna(subset=["Fecha"])

    # Convert Fecha column to datetime
    df_redcap["Fecha"] = pd.to_datetime(df_redcap["Fecha"], format="%Y-%m-%d")

    # Display selection options, horizontally
    grouping = st.selectbox("Group by: ", options=["Month", "Quarter", "Year"])

    # Group the data based on user selection
    if grouping == "Year":
        df_redcap["Group"] = df_redcap["Fecha"].dt.to_period("Y").apply(lambda r: r.start_time)
        title = "Yearly"
    elif grouping == "Month":
        df_redcap["Group"] = df_redcap["Fecha"].dt.to_period("M").apply(lambda r: r.start_time)
        title = "Monthly"
    elif grouping == "Quarter":
        df_redcap["Group"] = df_redcap["Fecha"].dt.to_period("Q").apply(lambda r: r.start_time)
        title = "Quarterly"

    # Aggregate data
    agg_data = df_redcap.groupby("Group").size().reset_index(name="Sample Count")

    # Prepare the data for plotting
    agg_data["Group"] = agg_data["Group"].astype(str)  # Convert Group to string for proper labeling
    agg_data["Cumulative Count"] = agg_data["Sample Count"].cumsum()  # Calculate cumulative cases

    # Create a bar chart for sample counts
    bars = alt.Chart(agg_data.reset_index()).mark_bar(color="skyblue").encode(
        x=alt.X("Group:N", title="Date", sort=None),
        y=alt.Y("Sample Count:Q", title="Number of Samples")
    )

    # Create a line chart for cumulative counts
    line = alt.Chart(agg_data.reset_index()).mark_line(color="orange", point=True).encode(
        x=alt.X("Group:N", title="Date", sort=None),
        y=alt.Y("Cumulative Count:Q", title="Accumulated Samples")
    )

    # Combine the bar chart, line chart, and label
    combined_chart = alt.layer(bars, line).resolve_scale(
        y="independent"  # Independent scales for bar and line charts
    ).properties(
        width=700,  # Set the width of the chart
        height=400  # Set the height of the chart
    )

    # Display the chart
    st.altair_chart(combined_chart, use_container_width=True)