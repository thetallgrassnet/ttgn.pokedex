"""Module for translating CSV data from Veekun for ttgn.pokedex."""
import csv
import pathlib
from urllib.request import urlopen

value_mappings = {
    'local_language_id': {
        '1': '2',
        '2': '4',
        '3': '6',
        '4': '10',
        '5': '14',
        '6': '17',
        '7': '15',
        '8': '16',
        '9': '5',
        '11': '1',
        '12': '9',
    },
    'version_id': {
        '1': '1',
        '2': '2',
        '3': '3',
        '4': '4',
        '5': '5',
        '6': '6',
        '7': '7',
        '8': '8',
        '9': '11',
        '10': '9',
        '11': '10',
        '12': '12',
        '13': '13',
        '14': '14',
        '15': '15',
        '16': '16',
        '17': '17',
        '18': '18',
        '21': '19',
        '22': '20',
        '23': '21',
        '24': '22',
        '25': '23',
        '26': '24',
        '27': '25',
        '28': '26',
        '29': '27',
        '30': '28',
    }
}


class VeekunLoader:
    """Load Veekun CSV data from GitHub."""

    def __init__(self, table):
        self.uri = ('https://raw.githubusercontent.com/veekun/pokedex/master'
                    '/pokedex/data/csv/{}.csv').format(table)

    def readlines(self):
        """Generator yielding Unicode string rows from the CSV data file."""
        with urlopen(self.uri) as data:
            for row in data:
                yield row.decode('utf-8')

    def reader(self):
        """Creates a csv.DictReader for the CSV data."""
        return csv.DictReader(self.readlines())


class MigrationWriter:
    """Write ttgn.pokedex data migration from Veekun data."""

    def __init__(self, veekun, rev, model):
        self.data_path = pathlib.Path(
            pathlib.Path(__file__).parent, 'data',
            '{}_upgrade_insert_{}_veekun.csv'.format(rev, model))

        if self.data_path.is_file():
            raise FileExistsError

        self.reader = veekun.reader()
        self.fieldnames = ['id', *self.reader.fieldnames]
        self.value_mapped_fields = self.fieldnames & value_mappings.keys()

    def write_migration(self, transform):
        """Write the data migration file."""
        _id = 0

        with self.data_path.open('w', newline='') as data:
            writer = csv.DictWriter(data, fieldnames=self.fieldnames)
            writer.writeheader()

            for row in self.reader:
                try:
                    mapped_row = self._mapped_row(row)
                    transformed_row = transform(mapped_row)
                    _id += 1
                    writer.writerow({'id': _id, **transformed_row})
                except UnmappedValueError:
                    continue

    def _mapped_row(self, row):
        """Perform key and value mappings on the Veekun data."""
        try:
            for field in self.value_mapped_fields:
                row[field] = value_mappings[field][row[field]]

            return row
        except KeyError:
            raise UnmappedValueError


class UnmappedValueError(Exception):
    """Attempted to map an unmapped value, meaning the Veekun data is missing
    from ttgn.pokedex."""
    pass


def create_migration_from_veekun(veekun_table,
                                 rev,
                                 model,
                                 transform=lambda r: r):
    """Create a ttgn.pokedex data migration from Veekun CSV data."""
    try:
        veekun = VeekunLoader(veekun_table)
        writer = MigrationWriter(veekun, rev, model)
        writer.write_migration(transform)
    except FileExistsError:
        return
