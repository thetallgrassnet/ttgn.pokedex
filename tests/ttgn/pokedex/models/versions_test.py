# pylint: disable=no-self-use
"""Test the ttgn.pokedex.models.versions module."""
from ttgn.pokedex.models import versions


class TestGeneration:
    """Test the ttgn.pokedex.models.versions.Generation class."""

    def test_migration(self, pokedex):
        """Test that data migrations are run correctly for the model."""
        query = pokedex.query(versions.Generation)
        assert query.count() == 7

    def test_version_groups(self, pokedex):
        """Test the version_groups association on a Generation object."""
        query = pokedex.query(versions.VersionGroup).join(
            versions.Generation.version_groups).filter(
                versions.Generation.id_ == 1)
        assert query.count() == 2

    def test_versions(self, pokedex):
        """Test the versions association on a Generation object."""
        query = pokedex.query(versions.Version).join(
            versions.Generation.versions).filter(versions.Generation.id_ == 1)
        assert query.count() == 3

    def test_str(self, pokedex):
        """Test the ttgn.pokedex.models.versions.Generation.__str__()
        method."""
        generation = pokedex.query(versions.Generation).get(1)
        assert str(generation) == 'Generation 1'


class TestVersionGroup:
    """Test the ttgn.pokedex.models.versions.VersionGroup class."""

    def test_migration(self, pokedex):
        """Test that data migrations are run correctly for the model."""
        query = pokedex.query(versions.VersionGroup)
        assert query.count() == 16

    def test_generation(self, pokedex):
        """Test the generation association on a VersionGroup object."""
        query = pokedex.query(versions.Generation).join(
            versions.VersionGroup.generation).filter(
                versions.VersionGroup.id_ == 1)
        generation = query.one()
        assert generation.id_ == 1

    def test_versions(self, pokedex):
        """Test the versions association on a VersionGroup object."""
        query = pokedex.query(versions.Version).join(
            versions.VersionGroup.versions).filter(
                versions.VersionGroup.id_ == 1)
        assert query.count() == 2

    def test_str(self, pokedex):
        """Test the ttgn.pokedex.models.versions.VersionGroup.__str__()
        method."""
        version_group = pokedex.query(versions.VersionGroup).get(1)
        assert str(version_group) == 'RB'


class TestVersion:
    """Test the ttgn.pokedex.models.versions.Version class."""

    def test_migration(self, pokedex):
        """Test that data migrations are run correctly for the model."""
        query = pokedex.query(versions.Version)
        assert query.count() == 28

    def test_generation(self, pokedex):
        """Test the generation association on a Version object."""
        query = pokedex.query(versions.Generation).join(
            versions.Version.generation).filter(versions.Version.id_ == 1)
        generation = query.one()
        assert generation.id_ == 1

    def test_version_group(self, pokedex):
        """Test the version_group association on a Version object."""
        query = pokedex.query(versions.VersionGroup).join(
            versions.Version.version_group).filter(versions.Version.id_ == 1)
        version_group = query.one()
        assert version_group.id_ == 1

    def test_str(self, pokedex):
        """Test the ttgn.pokedex.models.versions.Version.__str__() method."""
        version = pokedex.query(versions.Version).get(1)
        assert str(version) == 'R'

    def test_translations(self, pokedex):
        """Test the insertion of versions.Version translations."""
        query = pokedex.query(versions.VersionTranslation)
        assert query.count() == 198
