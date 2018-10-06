"""Core-series game related models."""
import sqlalchemy as sa
from sqlalchemy.orm import relationship

from ttgn.pokedex.models.base import Base, belongs_to
from ttgn.pokedex.models.multilang import with_translations


class Generation(Base):
    """Model representing a core-series game generation."""

    def __str__(self):
        return 'Generation {}'.format(self.id_)


@belongs_to(Generation)
class VersionGroup(Base):
    """Model representing a group of versions within a core-series
    generation."""

    def __str__(self):
        return ''.join([v.acronym for v in self.versions])


@belongs_to(VersionGroup)
@with_translations(name=sa.Column(sa.Unicode, nullable=False))
class Version(Base):
    """Model representing a core-series game version."""
    acronym = sa.Column(sa.String(2), nullable=False, unique=True)

    generation = relationship(
        Generation,
        secondary=VersionGroup.__table__,
        uselist=False,
        backref='versions')

    def __str__(self):
        return self.acronym
