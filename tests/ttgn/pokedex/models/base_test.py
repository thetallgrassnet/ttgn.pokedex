"""Test the ttgn.pokedex.models.base module."""
# pylint: disable=no-self-use
from ttgn.pokedex.models.base import Language


class TestLanguage:
    """Test the ttgn.pokedex.models.base.Language class."""

    def test_migration(self, pokedex):
        """Test that data migrations are run correctly for the model."""
        query = pokedex.query(Language)
        assert query.count() == 17
