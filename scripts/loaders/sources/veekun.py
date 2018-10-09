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
"""dict of str: dict of str: str: Mappings of value differences between
Veekun and ttgn.pokedex data."""


class VeekunSource(BaseSource):
    """Veekun CSV data source for external data.

    Parameters
    ----------
    table : str
        Name of Veekun table that contains the source data.
    ref : str, optional
        Git ref of the version of the data to retrieve. Defaults to
        ``master``.

    Attributes
    ----------
    url : str
        URL to the raw CSV file on GitHub containing the source data.
    value_mapped_fields : list of str
        List of fields for which value mapping should be performed.

    """
    __sourcename__ = 'veekun'

    def __init__(self, table, ref='master'):
        super().__init__()
        self.url = ('https://raw.githubusercontent.com/veekun/pokedex/'
                    '{}/pokedex/data/csv/{}.csv').format(ref, table)
        self.value_mapped_fields = self.fieldnames & VALUE_MAPPINGS.keys()

    def _map_rows(self, rows):
        """Perform known data mappings and yield mapped rows of data.

        If a value is encountered for which no mapping exists, continue on to
        the next row from the source data. The row will be excluded from the
        resulting data migration.

        Parameters
        ----------
        rows : iterable of dict of str: str
            CSV-parsed rows of data from the source file.

        Yields
        ------
        row : dict of str: str
            Row of value-mapped CSV-parsed data.

        """
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
        """Convert each binary line to a Unicode string.

        Yields
        ------
        line : str
            UTF-8 encoded CSV-formatted line of data from the source file.

        """
        for line in data:
            yield line.decode('utf-8')
