"""SQLAlchemy model declarative base configuration."""
import inflect
import sqlalchemy.orm
from sqlalchemy.ext import declarative

from ttgn.pokedex.utils import snake_case

engine = inflect.engine()


def belongs_to(target, name=None, backref=None, nullable=False):
    """Decorator that creates a foreign key column and relationship on the
    decorated class pointing to the target class.

    If a name or backref parameter are not provided, the name of the target
    class and the pluralized name of the decorated class are used to generate
    the relationship and backref name respectively."""

    def decorator(cls):
        _name = snake_case(target.__name__) if name is None else name
        _name_id = '{}_id'.format(_name)
        _backref = cls.__pluralname__ if backref is None else backref

        setattr(
            cls, _name_id,
            sqlalchemy.Column(
                sqlalchemy.Integer,
                sqlalchemy.ForeignKey(target.id),
                nullable=nullable))

        setattr(
            cls, _name,
            sqlalchemy.orm.relationship(
                target,
                backref=_backref,
                foreign_keys=[getattr(cls, _name_id)]))

        return cls

    return decorator


class Base:
    """Base class for SQLAlchemy declarative base."""
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)

    # pylint: disable=no-self-argument
    @declarative.declared_attr
    def __pluralname__(cls):
        name = snake_case(cls.__name__).rsplit('_', 1)
        name.append(engine.plural(name.pop()))
        return '_'.join(name)

    # pylint: disable=no-self-argument
    @declarative.declared_attr
    def __tablename__(cls):
        """Generate the table name from the full module path of a model
        class."""
        return "{}_{}".format(
            cls.__module__.replace('.', '_'), cls.__pluralname__)


Base = declarative.declarative_base(cls=Base)
