"""
Utility functions for database access.
"""
from database.config import DEFAULT_DB_CONNECTION_STRING
from database.database import Database

# Singleton database instance for reuse
_db_instance = None


def get_database(connection_string=None, echo=False):
    """
    Get a database instance, reusing a singleton instance by default.

    Args:
        connection_string: SQLAlchemy connection string (defaults to the config value)
        echo: Whether to echo SQL (useful for debugging)

    Returns:
        Database instance
    """
    global _db_instance

    # Use default connection string if none provided
    if connection_string is None:
        connection_string = DEFAULT_DB_CONNECTION_STRING

    # Create new instance if needed
    if _db_instance is None:
        _db_instance = Database(connection_string=connection_string, echo=echo)
        _db_instance.create_tables()

    return _db_instance
