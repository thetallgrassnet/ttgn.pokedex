class TestGeneration(object):
    def test_migration(self, pokedex):
        from ttgn.pokedex.models.versions import Generation

        query = pokedex.query(Generation)
        assert len(query.all()) == 7
