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
st.title("Welcome to NBA Analytics Hub", anchor=False)

st.markdown("""
<div style="font-size: 30px; margin-bottom: 30px;">
<p>Your all-in-one destination for NBA statistics and betting insights</p>
</div>
""", unsafe_allow_html=True)


# Main features section
st.header("Explore Features", anchor=False)

col1, col2 = st.columns(2)

with col1:
    with st.container():
        col1_1, col1_2 = st.columns([1, 1], vertical_alignment="center")
        with col1_1:
            st.markdown("""
            <h3 style="font-size: 24px; font-weight: 600;">📊Statistics Visualizer-Playoff</h3>
            """, unsafe_allow_html=True)
        with col1_2:
            st.page_link("nba_playoff_stats_visualizer/playoff_visualizer_page.py",
                         label="Show me")

        st.markdown("""
        <div style="font-size: 24px; background-color: #f0f2f6; padding: 20px; border-radius: 10px; min-height: 300px; height: auto; overflow: auto;">
            <h3 style="color: #0066cc;">Detailed Team & Player Insights</h3>
            <ul>
                <li>Game-by-game performance breakdowns</li>
                <li>Player statistics with interactive charts</li>
                <li>Historical playoff data dating back to 2015</li>
                <li>Key performance trends to inform your betting</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)


with col2:
    with st.container():
        col2_1, col2_2 = st.columns([1, 1], vertical_alignment="center")
        with col2_1:
            st.markdown("""
            <h3 style="font-size: 24px; font-weight: 600;"> 🟢 LIVE: Betting Odds Analysis</h3>
            """, unsafe_allow_html=True)
        with col2_2:
            st.page_link("betting_odds/betting_odds_page.py",
                         label="Show me")
        st.markdown("""
        <div style="font-size: 24px; background-color: #f0f2f6; padding: 20px; border-radius: 10px; min-height: 300px; height: auto; overflow: auto;">
            <h4 style="color: #0066cc;">Real-time Odds Comparison</h4>
            <ul>
                <li>Compare odds across major sportsbooks</li>
                <li>Track line movements to spot value</li>
                <li>Player prop betting insights</li>
            </ul>
            <p style="font-weight: bold; font-size: 18px; margin-top: 30px;">
            Make more informed betting decisions by combining statistical data with real-time odds.
            </p>
        </div>
        """, unsafe_allow_html=True)

# Getting started section
st.header("Getting Started")
st.markdown("""
<div style="font-size: 17px; margin-bottom: 20px;">
<p>To begin exploring the app, use the navigation in the sidebar to select which section you'd like to view:</p>
<ol>
    <li><strong>Playoff Visualizer</strong> - Deep dive into playoff statistics and performance metrics</li>
    <li><strong>Betting Odds</strong> - Explore and compare current betting lines and odds</li>
</ol>
</div>
""", unsafe_allow_html=True)

# About section
st.markdown("---")
st.subheader("About This Tool")
st.markdown("""
<div style="font-size: 16px;">
<p>This NBA Playoff Analytics Hub is built for sports bettors and NBA enthusiasts who want to make data-driven decisions. 
All statistics are sourced directly from official NBA data.</p>

<p>Have questions or suggestions? Use the feedback form in the sidebar to let me know how we can improve!</p>
</div>
""", unsafe_allow_html=True)

# Add attribution footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 0.8em;'>Data provided by NBA API. Application created by Yi-An T.</div>",
    unsafe_allow_html=True
)
