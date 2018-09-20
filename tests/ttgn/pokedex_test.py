class TestPokedex(object):
    def test_migrate(self, pokedex):
        query = pokedex.query('version_num from alembic_version')
        assert query.all() == [('317f62cffc9a', )]

    def test_query(self, pokedex):
        query = pokedex.query('1')
        assert str(query) == 'SELECT 1'
        assert query.all() == [(1, )]
