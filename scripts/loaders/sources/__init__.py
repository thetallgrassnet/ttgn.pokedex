"""External data sources for data migration import."""
import csv
from abc import ABC, abstractmethod


class BaseSource(ABC):
    """Abstract external data source."""

    def __init__(self):
        self._reader = None

    @property
    @classmethod
    @abstractmethod
    def __sourcename__(cls):
        """Source name for inclusion in the data migration file name."""
        pass

    def __str__(self):
        return self.__sourcename__

    @abstractmethod
    def open(self):
        """Return an iterable object that yields lines from the source data."""
        pass

    @property
    def fieldnames(self):
        """Return a list of fieldnames included in the data."""
        return self._get_reader().fieldnames

    @property
    def reader(self):
        """Yield a series of OrderedDicts representing parsed rows of data."""
        yield from self._map_rows(self._get_reader())

    def _get_reader(self):
        """Create (if it hasn't been) and return a csv.DictReader for the lines
        of data from the raw source."""
        if self._reader is None:
            self._reader = csv.DictReader(self._readlines())

        return self._reader

    # pylint: disable=no-self-use
    def _map_rows(self, rows):
        """Perform data mapping on and yield the parsed OrderedDict
        representing each row of data."""
        yield from rows

    def _readlines(self):
        """Yield lines of transformed data from the raw source."""
        with self.open() as data:
            yield from self._transform_data(data)

    # pylint: disable=no-self-use
    def _transform_data(self, data):
        """Transform each raw line of data into a CSV-formatted row."""
        yield from data
