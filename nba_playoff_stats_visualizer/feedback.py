import streamlit as st

from data_access.g_sheet_connection import send_feedback_to_sheets


def render_feedback_sidebar():
    """
    Function to render the feedback section in the sidebar.
    This will be called from each page to ensure consistent feedback functionality.
    """

    st.sidebar.header("Welcome to Leave Feedback")

    # Create a form for the feedback
    with st.sidebar.form(key="feedback_form"):
        st.markdown(
            "<p style='font-size: 0.85em; color: #666; margin-top: 0;'>"
            "If you provide your email, we'll send you updates about new features and improvements!</p>", unsafe_allow_html=True)

        # Optional name field
        name = st.text_input("Your Name (Optional)")
        email = st.text_input("Your Email (Optional)")

        # Feedback text area
        feedback = st.text_area("Your Feedback", height=150, max_chars=500,
                                placeholder="Please share your thoughts, suggestions, or report any issues...")

        # Submit button
        submit_button = st.form_submit_button(label="Submit Feedback")

        # Handle form submission
        if submit_button:
            if feedback:  # Make sure there's feedback text
                feedback_data = {
                    "name": name if name else "Anonymous",
                    "email": email if email else "",
                    "feedback": feedback,
                }

                # Show a spinner while submitting
                with st.spinner("Submitting your feedback..."):
                    success = send_feedback_to_sheets(feedback_data)

                if success:
                    st.success(
                        "Thank you for your feedback! Your input helps us improve.")
                else:
                    st.error(
                        "There was an issue submitting your feedback. Please try again later.")
            else:
                st.warning("Please enter some feedback before submitting.")
