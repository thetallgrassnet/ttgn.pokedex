"""Translation-related models and utility functions."""
import sqlalchemy

from .base import Base


class Language(Base):
    """Model representing an IANA language subtag for translation
    identification."""
    order = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, unique=True)
    language = sqlalchemy.Column(sqlalchemy.String(3), nullable=False)
    script = sqlalchemy.Column(sqlalchemy.String(8))
    region = sqlalchemy.Column(sqlalchemy.String(2))
    variant = sqlalchemy.Column(sqlalchemy.String(16))
