class TestPokedex(object):
    def test_query(self, pokedex):
        query = pokedex.query('1')
        assert str(query) == 'SELECT 1'
        assert query.all() == [(1, )]
