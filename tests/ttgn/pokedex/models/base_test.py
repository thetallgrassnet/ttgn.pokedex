from ttgn.pokedex.models.base import Language


class TestLanguage(object):
    def test_migration(self, pokedex):
        query = pokedex.query(Language)
        assert query.count() == 17
