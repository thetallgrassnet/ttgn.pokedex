"""Translation-related models and utility functions."""
import sys

import sqlalchemy
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import case

from ttgn.pokedex.utils import snake_case

from .base import Base, belongs_to


class Language(Base):
    """Model representing an IANA language subtag for translation
    identification."""
    order = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, unique=True)
    language = sqlalchemy.Column(sqlalchemy.String(3), nullable=False)
    script = sqlalchemy.Column(sqlalchemy.String(8))
    region = sqlalchemy.Column(sqlalchemy.String(2))
    variant = sqlalchemy.Column(sqlalchemy.String(16))

    @hybrid_property
    def subtag(self):
        return '-'.join(
            k for k in [self.language, self.script, self.region, self.variant]
            if k is not None)

    @subtag.expression
    def subtag(cls):
        return cls.language + \
            case([(cls.script != None, '-' + cls.script)], else_='') + \
            case([(cls.region != None, '-' + cls.region)], else_='') + \
            case([(cls.variant != None, '-' + cls.variant)], else_='')

    def __str__(self):
        return self.subtag


def with_translations(**kwargs):
    """Decorator that creates a translation table for the decorated model with
    the given columns, and creates relationships and association proxies for the
    translated columns."""

    def decorator(cls):
        translations = type('{}Translation'.format(cls.__name__), (Base, ), {})
        translations = belongs_to(cls, backref='translations')(translations)
        translations = belongs_to(
            Language, name='local_language')(translations)
        translations.__table__.append_constraint(
            sqlalchemy.UniqueConstraint(
                '{}_id'.format(snake_case(cls.__name__)), 'local_language_id'))

        for attr, column in kwargs.items():
            if not isinstance(column, sqlalchemy.Column):
                raise TypeError(
                    '{} expected to be a sqlalchemy.Column, was {}'.format(
                        attr, column))

            setattr(translations, attr, column)
            setattr(cls, attr, association_proxy('translations', attr))

        setattr(sys.modules[cls.__module__], translations.__name__,
                translations)

        return cls

    return decorator


Language = with_translations(
    name=sqlalchemy.Column(sqlalchemy.Unicode(64), nullable=False))(Language)
