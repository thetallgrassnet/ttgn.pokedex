import sqlalchemy.orm

from .base import Base


class Generation(Base):
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)

    def __str__(self):
        return 'Generation {}'.format(self.id)


class VersionGroup(Base):
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    generation_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey(Generation.__table__.columns.id),
        nullable=False)

    generation = sqlalchemy.orm.relationship(
        Generation, backref='version_groups')

    def __str__(self):
        return ''.join([v.acronym for v in self.versions])


class Version(Base):
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    version_group_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey(VersionGroup.__table__.columns.id),
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
