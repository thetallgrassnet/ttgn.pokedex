"""Handles database connection and session management for Pokédex instances."""
import contextlib
import logging
import os

import alembic.command
import alembic.config
import sqlalchemy.orm

base_path = os.path.realpath(
    os.path.join(os.path.dirname(__file__), '..', '..'))


class Pokedex:
    """Wrapper for the SQLAlchemy database engine and session object."""

    def __init__(self, uri=None, migrate=True, debug=False):
        """Initialize the database if necessary, and create the engine.

        Args:
            uri (str): Database connection string to use. Defaults to an on-
                disk SQLite database ``pokedex.sqlite`` in the root directory
                of the Pokédex project.
            migrate (bool): If True, automatically run database migrations on
                instantiation.
            debug (bool): If True, output detailed SQLAlchemy debug logging.
        """
        self.debug = debug
        self.logger = logging.getLogger(__name__)

        if uri is None:
            uri = 'sqlite:///{}'.format(
                os.path.join(base_path, 'pokedex.sqlite3'))

        self.logger.info('Using Pokédex database at {}'.format(uri))
        engine = sqlalchemy.create_engine(uri, echo=self.debug)

        self._Session = sqlalchemy.orm.sessionmaker(bind=engine)

        if migrate:
            alembic_cfg = alembic.config.Config(
                os.path.join(base_path, 'alembic.ini'))
            alembic_cfg.attributes['connectable'] = engine

            self.logger.debug('Running migrations')
            alembic.command.upgrade(alembic_cfg, 'head')

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
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
