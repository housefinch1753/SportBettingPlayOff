import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from ui_component.style_utils import load_css

# Load CSS styles
load_css()

# Set page title and description
st.title("WNBA Player Props Analysis")
st.markdown("""
This page provides analysis and insights for WNBA player props, helping you make more informed betting decisions.
""")

# Sidebar filters
st.sidebar.header("Filters")

# Date range selector
today = datetime.now()
default_start_date = today - timedelta(days=30)
start_date = st.sidebar.date_input("Start Date", default_start_date)
end_date = st.sidebar.date_input("End Date", today)

# Player selection
# TODO: Add player selection dropdown once we have the data source

# Main content area
st.header("Player Performance Analysis")

# Placeholder for future content
st.info("""
This section will include:
- Player performance trends
- Historical performance against specific teams
- Home/Away splits
- Recent form analysis
""")

# Add a placeholder for the main visualization
st.plotly_chart(
    go.Figure().update_layout(
        title="Player Performance Metrics",
        xaxis_title="Date",
        yaxis_title="Performance Metric",
        template="plotly_white"
    )
)

# Add a section for detailed statistics
st.header("Detailed Statistics")
st.markdown("""
Detailed statistics and analysis will be displayed here, including:
- Points per game
- Rebounds per game
- Assists per game
- Shooting percentages
- Advanced metrics
""")

# Add floating button at the bottom
if st.button("← Back to WNBA Betting Odds"):
    st.switch_page("betting_odds/wnba_betting_odds_page.py")

