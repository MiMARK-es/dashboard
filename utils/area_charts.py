import streamlit as st
import pandas as pd
import plotly.graph_objects as go
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

    # Filter fecha before 2018
    df_redcap = df_redcap[df_redcap["Fecha"].dt.year >= 2018]

    # Display selection options using Streamlit radio buttons
    grouping = st.radio("Group by:", options=["Month", "Quarter", "Year"], horizontal=True)

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
    agg_data["Group"] = agg_data["Group"].astype(str)  # Convert Group to string for proper labeling
    agg_data["Cumulative Count"] = agg_data["Sample Count"].cumsum()  # Calculate cumulative cases

    # Calculate axis ranges
    x_range = agg_data["Group"].tolist()  # Use all unique group values for x-axis
    y_max = max(agg_data["Cumulative Count"])  # Maximum y-value
    y_range = [0, y_max + int(0.1 * y_max)]  # Allow a 10% buffer above the maximum

    # x_texts are month names for monthly grouping, quarter names for quarterly grouping, and years for yearly grouping
    x_texts = x_range.copy()
    if grouping == "Month":
        x_texts = [pd.to_datetime(x).strftime("%b %Y") for x in x_range]
    elif grouping == "Quarter":
        x_texts = [f"{x.year} Q{x.quarter}" for x in pd.to_datetime(x_range)]
    elif grouping == "Year":
        x_texts = [pd.to_datetime(x).strftime("%Y") for x in x_range]

    # Create a Plotly figure
    fig = go.Figure()

    # Add bar chart for sample counts
    fig.add_trace(
        go.Bar(
            x=agg_data["Group"],
            y=agg_data["Sample Count"],
            name="Sample Count",
            marker=dict(color="skyblue"),
        )
    )

    # Add line chart for cumulative counts
    fig.add_trace(
        go.Scatter(
            x=agg_data["Group"],
            y=agg_data["Cumulative Count"],
            mode="lines+markers",
            name="Accumulated Samples",
            line=dict(color="orange"),
        )
    )

    # Update layout to prevent negative values and constrain x-axis
    fig.update_layout(
        title=f"{title} Sample Count and Accumulated Samples",
        xaxis=dict(
            title="Date",
            categoryorder="array",  # Keeps the bars ordered based on the input data
            categoryarray=x_range,  # Ensures consistent ordering of x-axis labels
            tickangle=45,  # Rotates x-axis labels by 45 degrees for better readability
            tickmode="array",
            tickvals=x_range,  # Show all x-axis labels
            ticktext=x_texts,  # Use the formatted labels for the x-axis
        ),
        yaxis=dict(
            title="Count",
            range=y_range,  # Constrain y-axis range to prevent negative values
        ),
        legend_title="Legend",
        legend=dict(
            x=0,  # Horizontal position (0 = left, 1 = right)
            y=1,  # Vertical position (0 = bottom, 1 = top)
            bgcolor="rgba(255,255,255,0.5)",  # Optional: Semi-transparent background for better readability
            bordercolor="gray",  # Optional: Border color for the legend
            borderwidth=1,  # Optional: Border width
        ),
        barmode="group",
        width=700,
        height=400,
        dragmode="pan",
    )

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)