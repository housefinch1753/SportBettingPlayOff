"""
Utility functions for database access.
"""
from database.config import DEFAULT_DB_CONNECTION_STRING
from database.database import Database

# Singleton database instances for each schema
_db_instances = {}


def get_database(schema: str, connection_string=None, echo=False):
    """
    Get a database instance for a specific schema.

    Args:
        schema: Database schema identifier
        connection_string: SQLAlchemy connection string (defaults to the config value)
        echo: Whether to echo SQL (useful for debugging)

    Returns:
        Database instance configured for the specified schema
    """
    global _db_instances

    # Use default connection string if none provided
    if connection_string is None:
        connection_string = DEFAULT_DB_CONNECTION_STRING

    # Create new instance if needed for this schema
    if schema not in _db_instances:
        _db_instances[schema] = Database(
            connection_string=connection_string,
            schema=schema,
            echo=echo
        )
        _db_instances[schema].create_tables()

    return _db_instances[schema]
