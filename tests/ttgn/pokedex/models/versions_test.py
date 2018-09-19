class TestGeneration(object):
    def test_migration(self, pokedex):
        from ttgn.pokedex.models.versions import Generation

        query = pokedex.query(Generation)
        assert len(query.all()) == 7

    def test_str(self, pokedex):
        from ttgn.pokedex.models.versions import Generation

        generation = pokedex.query(Generation).filter(Generation.id == 1).one()
        assert str(generation) == 'Generation 1'
