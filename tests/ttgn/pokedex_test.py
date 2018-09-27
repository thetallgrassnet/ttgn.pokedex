import pytest


class TestPokedex(object):
    def test_init_engine(self):
        import os

        from sqlalchemy import create_engine
        from ttgn.pokedex import Pokedex

        path = os.path.realpath(
            os.path.join(
                os.path.dirname(__file__), 'pokedex_test_init_engine.sqlite3'))
        uri = 'sqlite:///{}'.format(path)
        engine = create_engine(uri)
        pokedex = Pokedex(engine)

        try:
            query = pokedex.query('1')
            assert query.all() == [(1, )]
        finally:
            os.remove(path)

    def test_init_migrate_true(self, pokedex):
        query = pokedex.query('version_num from alembic_version')
        assert query.all() == [('088903c1ed2a', )]

    def test_query(self, pokedex):
        query = pokedex.query('1')
        assert str(query) == 'SELECT 1'
        assert query.all() == [(1, )]

    def test_session_scope_exception(self, pokedex):
        with pytest.raises(AssertionError):
            with pokedex.session_scope() as session:
                query = session.query('1')
                assert query.all() == [(2, )]
