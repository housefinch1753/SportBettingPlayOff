import datetime as dt
import logging
from datetime import datetime

import gspread
import streamlit as st
from google.oauth2.service_account import Credentials

logger = logging.getLogger(__name__)
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets'
]


def send_feedback_to_sheets(feedback_data):
    """
    Sends feedback data to a Google Sheet

    Args:
        feedback_data (dict): A dictionary containing feedback information

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Load credentials from secrets
        credentials = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=SCOPES
        )

        # Connect to Google Sheets
        client = gspread.authorize(credentials)
        # Open the spreadsheet by its ID (from secrets)
        sheet = client.open_by_key(st.secrets["feedback_sheet_id"]).sheet1

        # Prepare the data row
        timestamp_utc = datetime.now(
            dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        row = [
            timestamp_utc,
            feedback_data.get("name", "Anonymous"),
            feedback_data.get("email", "N/A"),
            feedback_data.get("feedback", ""),
        ]
        # Append the row to the sheet
        sheet.append_row(row)

        return True

    except Exception as e:
        logger.error(f"Error sending feedback to Google Sheets: {str(e)}")
        return False
