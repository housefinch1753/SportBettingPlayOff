"""
Shared Database class for managing connections to the database.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.base import Base


class Database:
    """
    Shared database class to handle connections and sessions across services.
    """

    def __init__(self, connection_string: str, echo: bool = False):
        """
        Initialize the database connection.

        Args:
            connection_string: SQLAlchemy database connection string
            echo: Whether to echo SQL queries (useful for debugging)
        """
        self.engine = create_engine(connection_string, connect_args={"options": "-c timezone=utc"}, echo=echo)
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self):
        """Create all tables defined in models"""
        Base.metadata.create_all(self.engine)

    def get_session(self):
        """Get a new session"""
        return self.Session()
