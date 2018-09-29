"""Translation-related models and utility functions."""
import sqlalchemy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import case

from .base import Base


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
