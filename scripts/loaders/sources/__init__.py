"""External data sources for data migration import."""
from abc import ABC, abstractmethod
from csv import DictReader


class BaseSource(ABC):
    """Abstract external data source."""

    def __init__(self):
        self.__reader = None

    @property
    @classmethod
    @abstractmethod
    def __sourcename__(cls):
        """str: Source name for inclusion in the data migration file name."""
        pass

    def __str__(self):
        return self.__sourcename__

    @property
    def fieldnames(self):
        """list of str: List of fieldnames included in the data."""
        return self._reader.fieldnames

    @property
    def reader(self):
        """iterator: Series of OrderedDicts representing parsed rows of
        data."""
        yield from self._map_rows(self._reader)

    # pylint: disable=no-self-use
    def _map_rows(self, rows):
        """Yield CSV-parsed rows from the source data.

        Parameters
        ----------
        rows : iterable of dict of str: str
            CSV-parsed rows of data from the source file.

        Yields
        ------
        row : dict of str: str
            CSV-parsed row of data from the source file.

        """
        yield from rows

    @abstractmethod
    def _open(self):
        """Open the source data file for iteration through each line.

        Returns
        -------
        iterable object

        """
        pass

    @property
    def _reader(self):
        """Create (if it hasn't been) and return a csv.DictReader for the
        source data.

        Returns
        -------
        csv.DictReader

        """
        if self.__reader is None:
            self.__reader = DictReader(self._readlines())

        return self.__reader

    def _readlines(self):
        """Reads lines of data from the source file.

        Yields
        ------
        line : str
            Line of data from the source file.

        """
        with self._open() as data:
            yield from self._transform_data(data)

    # pylint: disable=no-self-use
    def _transform_data(self, data):
        """Transform each raw line of data into a CSV-formatted row.

        Yields
        ------
        line : str
            CSV-formatted line of data from the source file.

        """
        yield from data
