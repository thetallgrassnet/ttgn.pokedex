import sqlalchemy.ext.declarative
import ttgn.pokedex.utils


class Base(object):
    @sqlalchemy.ext.declarative.declared_attr
    def __tablename__(cls):
        return "{}_{}".format(
            cls.__module__.replace('.', '_'),
            ttgn.pokedex.utils.snake_case(cls.__name__))


Base = sqlalchemy.ext.declarative.declarative_base(cls=Base)
