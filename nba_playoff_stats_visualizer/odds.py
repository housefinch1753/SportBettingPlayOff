import streamlit as st

# Hide the st.markdown anchor icon
st.html(
    "<style>[data-testid='stHeaderActionElements'] {display: none;}</style>")


# Title and description
st.title("NBA Playoff Betting Odds Data", anchor=False)

st.markdown("""
<div style="font-size: 18px;">
<h3 style="font-size: 28px;">💰 Real-Time NBA Betting Odds Analysis</h3>

<p>This page provides <strong>up-to-date betting odds data</strong> for NBA games. 
Compare odds across different sportsbooks and identify value betting opportunities.</p>

""", unsafe_allow_html=True)

# Placeholder for odds data - this will be implemented later
st.info("Odds data integration coming soon! "
        "This page will be populated with real-time betting odds from major sportsbooks in US.",
        )

# Add attribution footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 0.8em;'>Data provided by NBA API. Application created by Yi-An T.</div>",
    unsafe_allow_html=True
)
