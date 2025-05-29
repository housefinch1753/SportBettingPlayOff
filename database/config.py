"""
Shared database configuration to ensure consistent database connections across services.
"""
import streamlit as st

# read connection from local file
DEFAULT_DB_CONNECTION_STRING = st.secrets["database"]["connection_string"]
