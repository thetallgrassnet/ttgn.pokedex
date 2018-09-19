class TestPokedex(object):
    def test_migrate(self, pokedex):
        query = pokedex.query('version_num from alembic_version')
        assert query.all() == [('763b433aaf4a', )]

    def test_query(self, pokedex):
        query = pokedex.query('1')
        assert str(query) == 'SELECT 1'
        assert query.all() == [(1, )]
