"""
Shared SQLAlchemy declarative base for all ORM models.
"""

from sqlalchemy.ext.declarative import declarative_base

# Create a shared base class for all models
Base = declarative_base()
