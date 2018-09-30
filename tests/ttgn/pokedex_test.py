"""Test the ttgn.pokedex module."""
# pylint: disable=no-self-use
import pytest


class TestPokedex:
    """Test the ttgn.pokedex.Pokedex class."""

    class TestInit:
        """Test the ttgn.pokedex.Pokedex.__init__() method."""

        def test_init_engine(self):
            """Test providing a SQLAlchemy engine to the Pokedex
            constructor."""
            import os

            from sqlalchemy import create_engine
            from ttgn.pokedex import Pokedex

            path = os.path.realpath(
                os.path.join(
                    os.path.dirname(__file__),
                    'pokedex_test_init_engine.sqlite3'))
            uri = 'sqlite:///{}'.format(path)
            engine = create_engine(uri)
            pokedex = Pokedex(engine)

            try:
                query = pokedex.query('1')
                assert query.all() == [(1, )]
            finally:
                os.remove(path)

        def test_init_migrate_true(self, pokedex):
            """Test that all migrations are run at instantiation and that the
            database is at the latest revision."""
            query = pokedex.query('version_num from alembic_version')
            assert query.all() == [('1888d425f419', )]

    class TestQuery:
        """Test the ttgn.pokedex.Pokedex.query() method."""

        def test_query(self, pokedex):
            """Test performing a single query against the Pokédex database."""
            query = pokedex.query('1')
            assert str(query) == 'SELECT 1'
            assert query.all() == [(1, )]

    class TestSessionScope:
        """Test the ttgn.pokedex.Pokedex.session_scope() method."""

        def test_session_scope_exception(self, pokedex):
            """Test session rollback and exception re-raising from within a
            transactional session scope."""
            with pytest.raises(AssertionError):
                with pokedex.session_scope() as session:
                    query = session.query('1')
                    assert query.all() == [(2, )]
