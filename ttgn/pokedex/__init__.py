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

    Parameters
    ----------
    engine_or_uri : sqlalchemy.engine.Engine or str or None, optional
        Existing SQLAlchemy engine or database connection string to use.
        Defaults to an on-disk SQLite database ``pokedex.sqlite3`` in the
        root directory of the `ttgn.pokedex` package.
    migrate : bool, optional
        If True, automatically run database migrations on instantiation.
    alembic_cfg : alembic.config.Config or None, optional
        Existing Alembic configuration object against which to run
        migrations. Must include ``ttgn.pokedex:migrations`` in its
        ``version_locations`` list.
    debug : bool, optional
        If True, output detailed SQLAlchemy debug logging. Only used if a
        database connection string was passed as `engine_or_uri`.

    Attributes
    ----------
    debug : bool
    engine : sqlalchemy.engine.Engine
    logger : Logger

    """

    def __init__(self,
                 engine_or_uri=None,
                 migrate=True,
                 alembic_cfg=None,
                 debug=False):
        self.debug = debug
        self.logger = logging.getLogger(__name__)

        self.engine = self._get_database_engine(engine_or_uri)
        self._session = sessionmaker(bind=self.engine)

        if migrate:
            alembic_cfg = config.Config(
                pkg_resources.resource_filename(
                    __name__,
                    'alembic.ini')) if alembic_cfg is None else alembic_cfg
            alembic_cfg.attributes['connectable'] = self.engine

            self.logger.debug('Running migrations')
            command.upgrade(alembic_cfg, 'ttgn.pokedex@head')

    def query(self, *args, **kwargs):
        """Perform a single query against the database.

        All arguments are passed along to
        :meth:`sqlalchemy.orm.session.Session.query()`.

        Returns
        -------
        sqlalchemy.orm.query.Query

        """
        with self.session_scope() as session:
            return session.query(*args, **kwargs)

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of database operations.

        Yields a session object that can be used for a series of operations
        that are performed in a single transaction. The transaction is
        committed when the session goes out of scope, or rolled back if an
        exception is raised, and is ultimately closed.

        Yields
        ------
        :class:`sqlalchemy.orm.session.Session`

        Notes
        -----
        This method should only be used in advanced cases where a series of
        operations need to be treated as a discrete transaction, e.g. running
        multiple select queries in building a single HTTP response.

        """
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
        """Turns the `engine_or_uri` parameter to `__init__` into a
        SQLAlchemy engine.

        Parameters
        ----------
        engine_or_uri : sqlalchemy.engine.Engine or str or None

        Returns
        -------
        sqlalchemy.engine.Engine

        """
        if isinstance(engine_or_uri, Engine):
            return engine_or_uri

        uri = 'sqlite:///{}'.format(
            pkg_resources.resource_filename(
                __name__,
                'pokedex.sqlite3')) if engine_or_uri is None else engine_or_uri
        self.logger.info('Using Pokédex database at %s', uri)
        return create_engine(uri, echo=self.debug)
