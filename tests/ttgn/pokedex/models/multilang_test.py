"""Test the ttgn.pokedex.models.multilang module."""
# pylint: disable=no-self-use
from ttgn.pokedex.models.multilang import Language


class TestLanguage:
    """Test the ttgn.pokedex.models.multilang.Language class."""

    def test_migration(self, pokedex):
        """Test that data migrations are run correctly for the model."""
        query = pokedex.query(Language)
        assert query.count() == 17
