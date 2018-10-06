"""Translation-related models and utility functions."""
import sys

import sqlalchemy as sa
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import case

from ttgn.pokedex.models.base import Base, belongs_to
from ttgn.pokedex.utils import snake_case


class Language(Base):
    """Model representing an IANA language subtag for translation
    identification."""
    order = sa.Column(sa.Integer, nullable=False, unique=True)
    language = sa.Column(sa.String(3), nullable=False)
    script = sa.Column(sa.String(8))
    region = sa.Column(sa.String(2))
    variant = sa.Column(sa.String(16))

    @hybrid_property
    def subtag(self):
        """Combines the subtag components into a valid IANA language subtag."""
        return '-'.join(
            k for k in [self.language, self.script, self.region, self.variant]
            if k is not None)

    # pylint: disable=no-self-argument,singleton-comparison
    @subtag.expression
    def subtag(cls):
        """Enables querying the Language model by subtag values."""
        return cls.language + \
            case([(cls.script != None, '-' + cls.script)], else_='') + \
            case([(cls.region != None, '-' + cls.region)], else_='') + \
            case([(cls.variant != None, '-' + cls.variant)], else_='')

    def __str__(self):
        return self.subtag


def with_translations(**kwargs):
    """Decorator that creates a translation table for the decorated model with
    the given columns, and creates relationships and association proxies for
    the translated columns."""

    def decorator(cls):
        translations = type('{}Translation'.format(cls.__name__), (Base, ), {})
        translations = belongs_to(cls, backref='translations')(translations)
        translations = belongs_to(
            Language, name='local_language', backref=None)(translations)
        translations.__table__.append_constraint(
            sa.UniqueConstraint('{}_id'.format(snake_case(cls.__name__)),
                                'local_language_id'))

        for attr, column in kwargs.items():
            if not isinstance(column, sa.Column):
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
    name=sa.Column(sa.Unicode, nullable=False))(Language)
