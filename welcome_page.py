import streamlit as st

# Add responsive styling directly
st.markdown("""
<style>
/* Global responsiveness adjustments */
@media screen and (max-width: 992px) {
    div.row-widget.stHorizontal {
        flex-direction: column;
    }
    
    div.row-widget.stHorizontal > div {
        width: 100% !important;
        margin-bottom: 20px;
    }
    
    /* Font size adjustments for smaller screens */
    h1 {
        font-size: 28px !important;
    }
    
    h2 {
        font-size: 24px !important;
    }
    
    h3 {
        font-size: 20px !important;
    }
    
    p, li {
        font-size: 16px !important;
    }
    
    /* Custom container formatting */
    div[style*="font-size: 24px"] {
        font-size: 18px !important;
    }
    
    div[style*="font-size: 24px"] h3,
    div[style*="font-size: 24px"] h4 {
        font-size: 20px !important;
    }
    
    div[style*="font-size: 24px"] li {
        font-size: 16px !important;
    }
}

/* Extra small device adjustments */
@media screen and (max-width: 576px) {
    h1 {
        font-size: 24px !important;
    }
    
    h2 {
        font-size: 20px !important;
    }
    
    h3 {
        font-size: 18px !important;
    }
    
    p, li {
        font-size: 14px !important;
    }
    
    div[style*="font-size: 24px"] {
        font-size: 16px !important;
    }
    
    div[style*="font-size: 24px"] h3,
    div[style*="font-size: 24px"] h4 {
        font-size: 18px !important;
    }
    
    div[style*="font-size: 24px"] li {
        font-size: 14px !important;
    }
}

/* Custom container styling */
.css-1r6slb0, .css-keje6w {
    overflow: auto !important;
    height: auto !important;
}

/* Ensure markdown containers adjust properly */
div[data-testid="stMarkdownContainer"] > div {
    overflow-y: auto !important;
    height: auto !important;
}

/* Hide anchor elements */
[data-testid='stHeaderActionElements'] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

# Title and introduction
st.title("Welcome to Data-Driven Sportbetting Hub", anchor=False)

st.markdown("""
<div style="font-size: 30px; margin-bottom: 30px;">
<p>Your comprehensive destination for NBA & WNBA analytics and betting insights</p>
</div>
""", unsafe_allow_html=True)


# Main features section
st.header("Explore Features", anchor=False)

# First row: NBA and WNBA betting odds
col1, col2 = st.columns(2)

with col1:
    with st.container():
        col1_1, col1_2 = st.columns([1, 1], vertical_alignment="center")
        with col1_1:
            st.markdown("""
            <h3 style="font-size: 22px; font-weight: 600;">⛹️‍♂️ NBA Betting Odds</h3>
            """, unsafe_allow_html=True)
        with col1_2:
            st.page_link("betting_odds/nba_betting_odds_page.py",
                         label="Show NBA")

        st.markdown("""
        <div style="font-size: 20px; background-color: #f0f2f6; padding: 20px; border-radius: 10px; min-height: 280px; height: auto; overflow: auto;">
            <h4 style="color: #0066cc;">🟢 Real-Time Odds Analysis: 2024-25 PlayOff</h4>
            <ul>
                <li>Real-time odds comparison</li>
                <li>Major sportsbooks coverage</li>
                <li>Line movement tracking</li>
                <li>Player prop insights</li>
                <li>Value betting opportunities</li>
            </ul>
            <p style="font-weight: bold; font-size: 16px; margin-top: 20px; color: #28a745;">
            Stay ahead of the market with live betting data.
            </p>
        </div>
        """, unsafe_allow_html=True)

with col2:
    with st.container():
        col2_1, col2_2 = st.columns([1, 1], vertical_alignment="center")
        with col2_1:
            st.markdown("""
            <h3 style="font-size: 22px; font-weight: 600;">⛹️‍♀️ WNBA Betting Odds</h3>
            """, unsafe_allow_html=True)
        with col2_2:
            st.page_link("betting_odds/wnba_betting_odds_page.py",
                         label="Show WNBA")

        st.markdown("""
        <div style="font-size: 20px; background-color: #f0f2f6; padding: 20px; border-radius: 10px; min-height: 280px; height: auto; overflow: auto;">
            <h4 style="color: #0066cc;">🟢 Real-Time Odds Analysis: **2025 Regular** </h4>
            <ul>
                <li>Real-time odds comparison</li>
                <li>Major sportsbooks coverage</li>
                <li>Line movement tracking</li>
                <li>Player prop insights</li>
                <li>Value betting opportunities</li>
            </ul>
            <p style="font-weight: bold; font-size: 16px; margin-top: 20px; color: #28a745;">
            Stay ahead of the market with live betting data.
            </p>
        </div>
        """, unsafe_allow_html=True)

# Second row: Playoff Visualizer (first column)
st.markdown("<br>", unsafe_allow_html=True)
col3, col4 = st.columns(2)
with col3:
    with st.container():
        col3_1, col3_2 = st.columns([1, 1], vertical_alignment="center")
        with col3_1:
            st.markdown("""
            <h3 style="font-size: 22px; font-weight: 600;">📊 Playoff Visualizer</h3>
            """, unsafe_allow_html=True)
        with col3_2:
            st.page_link("nba_playoff_stats_visualizer/playoff_visualizer_page.py",
                         label="Analyze Data")

        st.markdown("""
        <div style="font-size: 20px; background-color: #e6f3ff; padding: 20px; border-radius: 10px; min-height: 280px; height: auto; overflow: auto;">
            <h4 style="color: #0066cc;">Deep Statistical Analysis</h4>
            <ul>
                <li>Game-by-game breakdowns</li>
                <li>Interactive performance charts</li>
                <li>Historical playoff data (2015+)</li>
                <li>Player & team analytics</li>
                <li>Trend identification</li>
            </ul>
            <p style="font-weight: bold; font-size: 16px; margin-top: 20px; color: #0066cc;">
            Make informed decisions with data-driven insights.
            </p>
        </div>
        """, unsafe_allow_html=True)

with col4:
    # Empty column for future features
    st.empty()

# Getting started section
st.header("Getting Started")
st.markdown("""
<div style="font-size: 17px; margin-bottom: 20px;">
<p>Navigate through our comprehensive sports betting platform using the sidebar menu:</p>
<ol>
    <li><strong>NBA Betting Odds</strong> - Live NBA lines, odds comparison, and market analysis</li>
    <li><strong>WNBA Betting Odds</strong> - Complete WNBA betting insights and opportunities</li>
    <li><strong>Playoff Visualizer</strong> - In-depth statistical analysis for both leagues</li>
</ol>
<p style="margin-top: 15px; font-weight: 600;">
🎯 <em>Combine real-time odds with historical performance data for smarter betting decisions.</em>
</p>
</div>
""", unsafe_allow_html=True)

# About section
st.markdown("---")
st.subheader("About This Platform")
st.markdown("""
<div style="font-size: 16px;">
<p>Our Data-Driven Sportbetting Hub serves both NBA and WNBA enthusiasts who demand comprehensive analytics. 
We combine official league statistics with real-time betting market data to give you the competitive edge.</p>

<p><strong>Key Benefits:</strong></p>
<ul>
    <li>✅ Real-time odds from multiple sportsbooks</li>
    <li>✅ Historical performance analytics</li>
    <li>✅ Both NBA and WNBA coverage</li>
    <li>✅ Mobile-responsive design</li>
    <li>✅ Data-driven insights</li>
</ul>

<p>Have questions or suggestions? Use the feedback form in the sidebar to help us improve your experience!</p>
</div>
""", unsafe_allow_html=True)

# Add attribution footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 0.8em;'>Data provided by NBA & WNBA APIs • Sports betting odds from multiple sources • Platform created by Yi-An T.</div>",
    unsafe_allow_html=True
)
