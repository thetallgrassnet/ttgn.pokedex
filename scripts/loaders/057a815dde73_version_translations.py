# pylint: disable=invalid-name
"""Import version translations from Veekun."""
from scripts.loaders import MigrationWriter
from scripts.loaders.sources.veekun import VeekunSource


class VeekunVersionTranslationsSource(VeekunSource):
    """Veekun data source for version translations."""

    def __init__(self):
        super().__init__(
            'version_names', ref='1d3dd33cbb4eb206f2c6d9ff2a78ee3b84a22764')

    @property
    def fieldnames(self):
        """Add ``id`` to the list of fieldnames from the source data."""
        return ['id', *super().fieldnames]

    def _map_rows(self, rows):
        """Override the ja-Hrkt local_language_id mapping and add the id
        field to each row."""
        _id = 0

        for row in super()._map_rows(rows):
            if row['local_language_id'] == '2':
                row['local_language_id'] = '1'

            _id += 1
            yield {'id': _id, **row}


def main():
    """Write the versions.VersionTranslation Veekun data migration."""
    source = VeekunVersionTranslationsSource()
    writer = MigrationWriter(
        source, '057a815dde73', 'versions.VersionTranslation', force=True)
    writer.write_migration()


if __name__ == '__main__':
    main()
