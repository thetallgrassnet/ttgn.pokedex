"""External data loaders for creating data migrations."""
import csv
import os

from pkg_resources import resource_filename


class MigrationWriter:
    """Data migration writer given an external source."""

    def __init__(self, source, rev, model, force=False):
        self.data_path = resource_filename(
            'ttgn.pokedex',
            'migrations/data/{}_upgrade_insert_{}_{}.csv'.format(
                rev, model, source))

        if os.path.exists(self.data_path) and not force:
            raise FileExistsError

        self.source = source

    def write_migration(self):
        """Write the source data to a migration file."""
        with open(self.data_path, 'w', newline='') as data:
            writer = csv.DictWriter(data, fieldnames=self.source.fieldnames)
            writer.writeheader()

            for row in self.source.reader:
                writer.writerow(row)
