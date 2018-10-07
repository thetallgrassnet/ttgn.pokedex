"""SQLAlchemy model declarative base configuration."""
from inflect import engine as inflector

import sqlalchemy as sa
from sqlalchemy.ext import declarative
from sqlalchemy.orm import backref, relationship

from ttgn.pokedex.utils import snake_case

_INFLECTOR = inflector()


def _backref_factory(name, cls, **kwargs):
    if name is None:
        return name

    name = cls.__pluralname__ if name is True else name
    return backref(name, **kwargs)


def belongs_to(target, name=None, backref_name=True, **backref_args):
    """Decorator that creates a foreign key column and relationship on the
    decorated class pointing to the target class.

    If a name or backref parameter are not provided, the name of the target
    class and the pluralized name of the decorated class are used to generate
    the relationship and backref name respectively."""

    def decorator(cls):
        _name = snake_case(target.__name__) if name is None else name
        _name_id = '{}_id'.format(_name)
        _backref = _backref_factory(backref_name, cls, **backref_args)

        setattr(
            cls, _name_id,
            sa.Column(sa.Integer, sa.ForeignKey(target.id_), nullable=False))

        setattr(
            cls, _name,
            relationship(
                target,
                backref=_backref,
                foreign_keys=[getattr(cls, _name_id)]))

        return cls

    return decorator


class Base:
    """Base class for SQLAlchemy declarative base."""
    id_ = sa.Column('id', sa.Integer, primary_key=True)

    @declarative.declared_attr
    def __pluralname__(cls):
        # pylint: disable=no-self-argument
        name = snake_case(cls.__name__).rsplit('_', 1)
        name.append(_INFLECTOR.plural(name.pop()))
        return '_'.join(name)

    @declarative.declared_attr
    def __tablename__(cls):
        # pylint: disable=no-self-argument
        """Generate the table name from the full module path of a model
        class."""
        return "{}_{}".format(
            cls.__module__.replace('.', '_'), cls.__pluralname__)


Base = declarative.declarative_base(cls=Base)
