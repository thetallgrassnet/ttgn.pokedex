from ttgn.pokedex.models import versions


class TestGeneration(object):
    def test_migration(self, pokedex):
        query = pokedex.query(versions.Generation)
        assert query.count() == 7

    def test_version_groups(self, pokedex):
        query = pokedex.query(versions.VersionGroup).join(
            versions.Generation.version_groups).filter(
                versions.Generation.id == 1)
        assert query.count() == 2

    def test_versions(self, pokedex):
        query = pokedex.query(versions.Version).join(
            versions.Generation.versions).filter(versions.Generation.id == 1)
        assert query.count() == 3

    def test_str(self, pokedex):
        generation = pokedex.query(versions.Generation).get(1)
        assert str(generation) == 'Generation 1'


class TestVersionGroup(object):
    def test_migration(self, pokedex):
        query = pokedex.query(versions.VersionGroup)
        assert query.count() == 16

    def test_generation(self, pokedex):
        query = pokedex.query(versions.Generation).join(
            versions.VersionGroup.generation).filter(
                versions.VersionGroup.id == 1)
        generation = query.one()
        assert generation.id == 1

    def test_versions(self, pokedex):
        query = pokedex.query(versions.Version).join(
            versions.VersionGroup.versions).filter(
                versions.VersionGroup.id == 1)
        assert query.count() == 2

    def test_str(self, pokedex):
        version_group = pokedex.query(versions.VersionGroup).get(1)
        assert str(version_group) == 'RB'


class TestVersion(object):
    def test_migration(self, pokedex):
        query = pokedex.query(versions.Version)
        assert query.count() == 28

    def test_generation(self, pokedex):
        query = pokedex.query(versions.Generation).join(
            versions.Version.generation).filter(versions.Version.id == 1)
        generation = query.one()
        assert generation.id == 1

    def test_version_group(self, pokedex):
        query = pokedex.query(versions.VersionGroup).join(
            versions.Version.version_group).filter(versions.Version.id == 1)
        version_group = query.one()
        assert version_group.id == 1

    def test_str(self, pokedex):
        version = pokedex.query(versions.Version).get(1)
        assert str(version) == 'Red'
