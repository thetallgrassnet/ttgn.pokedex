import sqlalchemy

from .base import Base


class Generation(Base):
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)

    def __str__(self):
        return 'Generation {}'.format(self.id)
