"""Test the ttgn.pokedex.models.multilang module."""
# pylint: disable=no-self-use
from ttgn.pokedex.models.multilang import Language


class TestLanguage:
    """Test the ttgn.pokedex.models.multilang.Language class."""

    def test_migration(self, pokedex):
        """Test that data migrations are run correctly for the model."""
        query = pokedex.query(Language)
        assert query.count() == 17

    def test_str(self, pokedex):
        """Test that the subtag is returned."""
        cn = pokedex.query(Language).get(12)
        assert str(cn) == 'cmn-latn-cn-pinyin'

    class TestSubtag:
        """Test the ttgn.pokedex.models.multilang.Language.subtag
        property."""

        def test_subtag_language_only(self, pokedex):
            """Test that the correct subtag with only the language identifier is
            returned."""
            en = pokedex.query(Language).get(5)
            assert en.subtag == 'en'

        def test_subtag_concatenated(self, pokedex):
            """Test that the concatenated subtag is returned."""
            ja = pokedex.query(Language).get(4)
            assert ja.subtag == 'ja-latn-x-official'

        def test_subtag_query(self, pokedex):
            """Test querying by subtag."""
            fr = pokedex.query(Language).filter(
                Language.subtag == 'fr-fr').one()
            assert fr.id == 14
