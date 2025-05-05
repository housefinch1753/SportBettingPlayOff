import streamlit as st

# Hide the st.markdown anchor icon
st.html(
    "<style>[data-testid='stHeaderActionElements'] {display: none;}</style>")


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
        col1_1, col1_2 = st.columns([1,1], vertical_alignment="center")
        with col1_1:
            st.markdown("""
            <h3 style="font-size: 24px; font-weight: 600;">📊Statistics Visualizer-Playoff</h3>
            """, unsafe_allow_html=True)
        with col1_2:
            st.page_link("nba_playoff_stats_visualizer/playoff_visualizer_page.py",
            label="Show me")

        st.markdown("""
        <div style="font-size: 24px; background-color: #f0f2f6; padding: 20px; border-radius: 10px; height: 300px;">
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
    st.markdown("""
    <h3 style="font-size: 24px; font-weight: 600;">🚧 Working In Progress: Betting Odds Analysis</h3>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size: 24px; background-color: #f0f2f6; padding: 20px; border-radius: 10px; height: 300px; opacity: 0.7; color: #666;">
        <h4 style="color: #6699cc;">Real-time Odds Comparison</h4>
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
