"""Handles database connection and session management for Pokédex instances."""
import contextlib
import os

import sqlalchemy.orm
import ttgn


class Pokedex:
    """Wrapper for the SQLAlchemy database engine and session object."""

    def __init__(self, uri=None):
        """Initialize the database if necessary, and create the engine.

        Args:
            uri (str): Database connection string to use. Defaults to an on-
                disk SQLite database ``pokedex.sqlite`` in the root directory
                of the Pokédex project.
        """
        if uri is None:
            path = os.path.realpath(os.path.join(ttgn.__path__[0], '..'))
            uri = 'sqlite:///{}'.format(os.path.join(path, 'pokedex.sqlite3'))

        engine = sqlalchemy.create_engine(uri)
        self._Session = sqlalchemy.orm.sessionmaker(bind=engine)

    def query(self, *args, **kwargs):
        """Perform a single query against the database."""
        with self.session_scope() as session:
            return session.query(*args, **kwargs)

    @contextlib.contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of database operations.

        This method should only be used in advanced cases where a series of
        operations need to be treated as a discrete transaction, e.g. running
        multiple select queries in building a single HTTP response."""
        session = self._Session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
