"""External data loaders for creating data migrations."""
from csv import DictWriter
from os.path import exists

from pkg_resources import resource_filename


class MigrationWriter:
    """Data migration writer given an external source."""

    def __init__(self, source, rev, model, force=False):
        self.data_path = resource_filename(
            'ttgn.pokedex',
            'migrations/data/{}_upgrade_insert_{}_{}.csv'.format(
                rev, model, source))

        if exists(self.data_path) and not force:
            raise FileExistsError

        self.source = source

    def write_migration(self):
        """Write the source data to a migration file."""
        with open(self.data_path, 'w', newline='') as data:
            writer = DictWriter(data, fieldnames=self.source.fieldnames)
            writer.writeheader()

            for row in self.source.reader:
                writer.writerow(row)
