import sqlalchemy
from sqlalchemy.ext import declarative

import ttgn.pokedex.utils


class Base(object):
    @declarative.declared_attr
    def __tablename__(cls):
        return "{}_{}".format(
            cls.__module__.replace('.', '_'),
            ttgn.pokedex.utils.snake_case(cls.__name__))


Base = declarative.declarative_base(cls=Base)


class Language(Base):
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    order = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, unique=True)
    language = sqlalchemy.Column(sqlalchemy.String(3), nullable=False)
    script = sqlalchemy.Column(sqlalchemy.String(8))
    region = sqlalchemy.Column(sqlalchemy.String(2))
    variant = sqlalchemy.Column(sqlalchemy.String(16))
