"""
Shared Database class for managing connections to the database.
"""

from sqlalchemy import create_engine, text, MetaData
from sqlalchemy.orm import sessionmaker
from database.base import Base


class Database:
    """
    Shared database class to handle connections and sessions across services.
    """

    def __init__(self, connection_string: str, schema: str = "public", echo: bool = False):
        """
        Initialize the database connection.

        Args:
            connection_string: SQLAlchemy database connection string
            schema: PostgreSQL schema name (e.g., 'nba', 'wnba')
            echo: Whether to echo SQL queries (useful for debugging)
        """
        self.schema = schema
        self.engine = create_engine(
            connection_string,
            connect_args={
                "options": f"-c timezone=utc -c search_path={schema},public"},
            echo=echo
        )
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self):
        """Create all tables defined in models in the specified schema."""
        # Create schema if it doesn't exist
        with self.engine.connect() as conn:
            conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {self.schema}"))
            conn.commit()

        # Create a schema-specific metadata object
        schema_metadata = MetaData(schema=self.schema)

        # Copy all tables from Base.metadata to schema_metadata
        for table in Base.metadata.tables.values():
            table.tometadata(schema_metadata)

        # Create all tables in the specified schema
        schema_metadata.create_all(self.engine)

    def get_session(self):
        """Get a new session"""
        return self.Session()
