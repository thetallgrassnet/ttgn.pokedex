"""SQLAlchemy model declarative base configuration."""
from inflect import engine as inflector

import sqlalchemy as sa
from sqlalchemy.ext import declarative
from sqlalchemy.orm import backref, relationship

from ttgn.pokedex.utils import snake_case

_INFLECTOR = inflector()


def _backref_factory(name, cls, **kwargs):
    """Generates a SQLAlchemy relationship back reference to `cls`.

    Parameters
    ----------
    name : bool or str
        Name of the back reference. If False, no back reference will be
        generated. If True, uses the
        :attr:`~ttgn.pokedex.models.base.Base.__pluralname__` of `cls`.
    cls : ttgn.pokedex.models.base.Base
        Model to which the back reference will point.
    **kwargs
        Additional arguments to pass to :func:`sqlalchemy.orm.backref`.

    Returns
    -------
    tuple or None
        Return value of :func:`sqlalchemy.orm.backref`, or None if `name` is
        False.

    """
    if not name:
        return None

    name = cls.__pluralname__ if name is True else name
    return backref(name, **kwargs)


def belongs_to(target, name=None, backref_name=True, **backref_args):
    """Decorator that creates a foreign key column and relationship on the
    decorated (child) class pointing to the target (parent) class.

    Parameters
    ----------
    target : .BaseClass
        Parent class in the `belongs_to` relationship.
    name : str, optional
        Name of the relationship on the child class. Defaults to the
        :func:`~ttgn.pokedex.utils.snake_case` formatted name of the `target`
        class.
    backref_name : bool or str, optional
        Name of the relationship on the parent class, created with
        :func:`sqlalchemy.orm.backref`. If True, defaults to the
        :attr:`~ttgn.pokedex.models.base.BaseClass.__pluralname__` of the
        child class.
    **backref_args
        Additional arguments passed to :func:`sqlalchemy.orm.backref`.

    """

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
                lazy='selectin',
                foreign_keys=[getattr(cls, _name_id)]))

        return cls

    return decorator


class BaseClass:
    """Base class for SQLAlchemy declarative base."""

    id_ = sa.Column('id', sa.Integer, primary_key=True)
    """int: Primary key, mapped to the ``id`` column of the table."""

    @declarative.declared_attr
    def __pluralname__(cls):
        # pylint: disable=no-self-argument
        """str: The :func:`~ttgn.pokedex.utils.snake_case` formatted plural
        form of the class name."""
        name = snake_case(cls.__name__).rsplit('_', 1)
        name.append(_INFLECTOR.plural(name.pop()))
        return '_'.join(name)

    @declarative.declared_attr
    def __tablename__(cls):
        # pylint: disable=no-self-argument
        """str: Table name, generated from the module path and
        :attr:`.__pluralname__` of the model class."""
        return "{}_{}".format(
            cls.__module__.replace('.', '_'), cls.__pluralname__)


Base = declarative.declarative_base(cls=BaseClass)
