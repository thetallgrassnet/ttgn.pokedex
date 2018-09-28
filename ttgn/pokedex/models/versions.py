"""Core-series game related models."""
import sqlalchemy.orm

from .base import Base, belongs_to


class Generation(Base):
    """Model representing a core-series game generation."""

    def __str__(self):
        return 'Generation {}'.format(self.id)


@belongs_to(Generation)
class VersionGroup(Base):
    """Model representing a group of versions within a core-series
    generation."""

    def __str__(self):
        return ''.join([v.acronym for v in self.versions])


@belongs_to(VersionGroup)
class Version(Base):
    """Model representing a core-series game version."""
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
    acronym = sqlalchemy.Column(
        sqlalchemy.String(2), nullable=False, unique=True)

    generation = sqlalchemy.orm.relationship(
        Generation,
        secondary=VersionGroup.__table__,
        uselist=False,
        backref='versions')

    def __str__(self):
        return self.name
