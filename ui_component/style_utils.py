import streamlit as st


def load_css():
    """Load CSS styles for the application."""
    # Define CSS directly
    css = """
    <style>
        /* Floating navigation button styles */
        .stButton > button {
            position: fixed !important;
            bottom: 20px !important;
            right: 20px !important;
            z-index: 1000 !important;
            background-color: #FF4B4B !important;
            color: white !important;
            padding: 10px 20px !important;
            border-radius: 5px !important;
            border: none !important;
            cursor: pointer !important;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2) !important;
        }

        .stButton > button:hover {
            background-color: #FF6B6B !important;
        }
    </style>
    """

    # Inject CSS
    st.markdown(css, unsafe_allow_html=True)
