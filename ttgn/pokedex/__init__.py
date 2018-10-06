"""Handles database connection and session management for Pokédex instances."""
import logging
from contextlib import contextmanager

import pkg_resources
from alembic import command, config

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker


class Pokedex:
    """Wrapper for the SQLAlchemy database engine and session object.

    Args:
        engine_or_uri (str|sqlalchemy.engine.Engine): Existing SQLAlchemy
            engine or database connection string to use. Defaults to an on-
            disk SQLite database ``pokedex.sqlite3`` in the root directory
            of the ``ttgn.pokedex`` package.
        migrate (bool): If True, automatically run database migrations on
            instantiation.
        alembic_cfg (alembic.config.Config): Existing Alembic configuration
            to use for running migrations. Must include the Pokédex
            migrations in its ``versions_location``.
        debug (bool): If True, output detailed SQLAlchemy debug logging.
            Mostly for development, and only used if an existing engine
            was not passed in with the ``engine_or_uri`` parameter.
    """

    def __init__(self,
                 engine_or_uri=None,
                 migrate=True,
                 alembic_cfg=None,
                 debug=False):
        self.debug = debug
        self.logger = logging.getLogger(__name__)

        engine = self._get_database_engine(engine_or_uri)
        self._session = sessionmaker(bind=engine)

        if migrate:
            alembic_cfg = config.Config(
                pkg_resources.resource_filename(
                    __name__,
                    'alembic.ini')) if alembic_cfg is None else alembic_cfg
            alembic_cfg.attributes['connectable'] = engine

            self.logger.debug('Running migrations')
            command.upgrade(alembic_cfg, 'ttgn.pokedex@head')

    def query(self, *args, **kwargs):
        """Perform a single query against the database. All arguments are passed
        along to the ``.query()`` method of a SQLAlchemy session."""
        with self.session_scope() as session:
            return session.query(*args, **kwargs)

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of database operations.

        This method should only be used in advanced cases where a series of
        operations need to be treated as a discrete transaction, e.g. running
        multiple select queries in building a single HTTP response."""
        session = self._session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def _get_database_engine(self, engine_or_uri):
        if isinstance(engine_or_uri, Engine):
            return engine_or_uri

        uri = 'sqlite:///{}'.format(
            pkg_resources.resource_filename(
                __name__,
                'pokedex.sqlite3')) if engine_or_uri is None else engine_or_uri
        self.logger.info('Using Pokédex database at %s', uri)
        return create_engine(uri, echo=self.debug)
