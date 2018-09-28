"""Core-series game related models."""
import sqlalchemy.orm

from .base import Base


class Generation(Base):
    """Model representing a core-series game generation."""

    def __str__(self):
        return 'Generation {}'.format(self.id)


class VersionGroup(Base):
    """Model representing a group of versions within a core-series
    generation."""
    generation_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey(Generation.id),
        nullable=False)

    generation = sqlalchemy.orm.relationship(
        Generation, backref='version_groups')

    def __str__(self):
        return ''.join([v.acronym for v in self.versions])


class Version(Base):
    """Model representing a core-series game version."""
    version_group_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey(VersionGroup.id),
        nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
    acronym = sqlalchemy.Column(
        sqlalchemy.String(2), nullable=False, unique=True)

    generation = sqlalchemy.orm.relationship(
        Generation,
        secondary=VersionGroup.__table__,
        uselist=False,
        backref='versions')
    version_group = sqlalchemy.orm.relationship(
        VersionGroup, backref='versions')

    def __str__(self):
        return self.name
