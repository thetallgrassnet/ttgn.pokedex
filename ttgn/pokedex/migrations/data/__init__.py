"""Utility methods for data migration processing."""
from csv import DictReader
from itertools import groupby
from re import match

from alembic.op import bulk_insert, execute
from pkg_resources import resource_listdir, resource_string, yield_lines

from sqlalchemy.sql.expression import bindparam

from ttgn.pokedex.utils import import_string


def load_data_migrations(rev, direction):
    """Loads and performs data migrations for a given revision and
    direction."""
    data_migrations = filter(
        lambda f: match(r'{}_{}_.*\.csv'.format(rev, direction), f),
        resource_listdir('ttgn.pokedex', 'migrations/data'))
    data = _read_data_from_migrations(data_migrations)

    for model in data:
        _perform_data_migration(model, data[model])


def _read_data_from_migrations(data_migrations):
    data = {}

    for filename in data_migrations:
        reader = MigrationReader(filename)
        model, operation, rows = reader.read_migration()
        data.setdefault(model, {}).setdefault(operation, []).extend(rows)

    return data


def _perform_data_migration_insert(table, rows):
    bulk_insert(table, rows)


def _perform_data_migration_update(table, rows):
    for keys, grouped_rows in groupby(rows, key=lambda r: r.keys()):
        stmt = table.update().where(table.c.id_ == bindparam('id')).values(
            {key: bindparam(key)
             for key in keys if not key == 'id'})
        execute(stmt, grouped_rows)


def _perform_data_migration_delete(table, rows):
    stmt = table.delete().where(table.c.id_ == bindparam('id'))
    execute(stmt, rows)


_DATA_MIGRATION_OPERATIONS = {
    'insert': _perform_data_migration_insert,
    'update': _perform_data_migration_update,
    'delete': _perform_data_migration_delete,
}


def _perform_data_migration(model, data):
    table = _import_model(model).__table__

    for operation, rows in data.items():
        _DATA_MIGRATION_OPERATIONS[operation](table, rows)


def _import_model(model_path):
    return import_string('ttgn.pokedex.models.{}'.format(model_path))


class MigrationReader:
    """Parse a data migration to get the model, operation, and data."""

    def __init__(self, filename):
        _match = match(
            r'[0-9a-f]{12}_(?:up|down)grade_'
            r'(insert|update|delete)_'
            r'([a-z_]+\.[A-Z][A-Za-z]+).*\.csv', filename)

        self.operation = _match.group(1)
        self.model = _match.group(2)
        self.filename = filename

    def read_migration(self):
        """Return the migration model, operation, and data."""
        return (self.model, self.operation, list(self._reader))

    @property
    def _reader(self):
        for row in DictReader(self._readlines()):
            yield {k: None if v == '' else v for k, v in row.items()}

    def _readlines(self):
        raw_data = resource_string('ttgn.pokedex',
                                   'migrations/data/{}'.format(self.filename))

        yield from yield_lines(raw_data.decode('utf-8'))
