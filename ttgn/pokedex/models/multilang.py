"""Translation-related models and utility functions."""
import sys

import sqlalchemy as sa
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.sql import case

from ttgn.pokedex.models.base import Base, belongs_to
from ttgn.pokedex.utils import snake_case


class Language(Base):
    """Model representing an IANA language subtag for translation
    identification.

    Attributes
    ----------
    order : int
        Display order for the listed language.
    language : str
        2- or 3-character IANA language code.
    script : str
        IANA script code.
    region : str
        2-character IANA region code.
    variant : str
        IANA variant code.
    name : :obj:`dict` of :obj:`str`: :class:`.LanguageTranslation`
        Translated language names mapped by :attr:`~.Language.subtag`.

    """
    order = sa.Column(sa.Integer, nullable=False, unique=True)
    language = sa.Column(sa.String(3), nullable=False)
    script = sa.Column(sa.String(8))
    region = sa.Column(sa.String(2))
    variant = sa.Column(sa.String(16))

    @hybrid_property
    def subtag(self):
        """str: Unique, valid IANA subtag for the `Language` instance."""
        return '-'.join(
            k for k in [self.language, self.script, self.region, self.variant]
            if k is not None)

    # pylint: disable=missing-docstring,no-self-argument,singleton-comparison
    @subtag.expression
    def subtag(cls):
        return cls.language + \
            case([(cls.script != None, '-' + cls.script)], else_='') + \
            case([(cls.region != None, '-' + cls.region)], else_='') + \
            case([(cls.variant != None, '-' + cls.variant)], else_='')

    def __str__(self):
        return self.subtag


def with_translations(**columns):
    """Decorator that creates a translations table for the decorated model.

    Creates a table mapped to a ``ModelTranslations`` class (given a
    decorated model class ``Model``) containing the provided `**columns`,
    with references to the :class:`.Language` and the decorated model. On the
    decorated model, creates an association proxy for each translated field
    that returns a dict of translations mapped by :attr:`~.Language.subtag`.

    Parameters
    ----------
    **columns : :obj:`dict` of :obj:`str`: :class:`sqlalchemy.schema.Column`
        Translatable columns to create in the translations table, typically
        of the :class:`sqlalchemy.types.Unicode` type.

    """

    def decorator(cls):
        Translations = type('{}Translation'.format(cls.__name__), (Base, ),
                            columns)
        Translations = belongs_to(
            cls,
            backref_name='translations',
            collection_class=attribute_mapped_collection('subtag'))(
                Translations)
        Translations = belongs_to(
            Language, name='local_language', backref_name=False)(Translations)
        Translations.__table__.append_constraint(
            sa.UniqueConstraint('{}_id'.format(snake_case(cls.__name__)),
                                'local_language_id'))

        setattr(Translations, 'subtag',
                association_proxy('local_language', 'subtag'))

        for attr in columns:
            setattr(cls, attr, association_proxy('translations', attr))

        setattr(sys.modules[cls.__module__], Translations.__name__,
                Translations)

        return cls

    return decorator


Language = with_translations(
    name=sa.Column(sa.Unicode, nullable=False))(Language)
