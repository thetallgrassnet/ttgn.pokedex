"""Veekun CSV data source and mappings for external data."""
from urllib.request import urlopen

from . import BaseSource

VALUE_MAPPINGS = {
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


class VeekunSource(BaseSource):
    """Veekun CSV data source for external data."""
    __sourcename__ = 'veekun'

    def __init__(self, table, ref='master'):
        super().__init__()
        self.url = ('https://raw.githubusercontent.com/veekun/pokedex/'
                    '{}/pokedex/data/csv/{}.csv').format(ref, table)
        self.value_mapped_fields = self.fieldnames & VALUE_MAPPINGS.keys()

    def _map_rows(self, rows):
        """Perform known data mappings."""
        for row in rows:
            try:
                for field in self.value_mapped_fields:
                    row[field] = VALUE_MAPPINGS[field][row[field]]

                yield row
            except KeyError:
                continue

    def _open(self):
        """Open the URL pointing to the CSV data."""
        return urlopen(self.url)

    def _transform_data(self, data):
        """Convert each binary line to a Unicode string."""
        for line in data:
            yield line.decode('utf-8')
