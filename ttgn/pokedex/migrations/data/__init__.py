"""Utility methods for data migration processing."""


def if_x_argument(arg, default):
    """Evaluates if a given x argument was passed to Alembic, using the given
    default if not."""
    from alembic import context
    return context.get_x_argument(as_dictionary=True).get(arg, default)


def load_data_migrations(rev, direction):
    """Loads and performs data migrations for a given revision and
    direction."""
    import re
    from pkg_resources import resource_listdir

    data_migrations = filter(
        lambda f: re.match(r'{}_{}_.*\.csv'.format(rev, direction), f),
        resource_listdir('ttgn.pokedex', 'migrations/data'))
    data = _read_data_from_migrations(data_migrations)

    for model in data:
        _perform_data_migration(model, data[model])


def _read_data_from_migrations(data_migrations):
    data = {}

    for file in data_migrations:
        import csv
        import re
        from pkg_resources import resource_string, yield_lines

        match = re.match(
            r'[0-9a-f]{12}_(?:up|down)grade_'
            r'(insert|update|delete)_'
            r'([a-z_]+\.[A-Z][A-Za-z]+).*\.csv', file)
        operation = match.group(1)
        model = match.group(2)

        data.setdefault(model, {})[operation] = []

        raw_data = resource_string('ttgn.pokedex',
                                   'migrations/data/{}'.format(file))
        reader = csv.DictReader(yield_lines(raw_data.decode('utf-8')))

        for row in reader:
            data[model][operation].append(_noneify_row(row))

    return data


def _noneify_row(row):
    """Interpret empty strings in a CSV row as None."""
    return {k: None if v == '' else v for k, v in row.items()}


def _perform_data_migration_insert(table, rows):
    from alembic.op import bulk_insert
    bulk_insert(table, rows)


def _perform_data_migration_update(table, rows):
    from itertools import groupby

    from alembic.op import execute
    from sqlalchemy.sql.expression import bindparam

    for keys, grouped_rows in groupby(rows, key=lambda r: r.keys()):
        stmt = table.update().where(table.c.id == bindparam('id')).values(
            {key: bindparam(key)
             for key in keys if not key == 'id'})
        execute(stmt, grouped_rows)


def _perform_data_migration_delete(table, rows):
    from alembic.op import execute
    from sqlalchemy.sql.expression import bindparam

    stmt = table.delete().where(table.c.id == bindparam('id'))
    execute(stmt, rows)


_data_migration_operations = {
    'insert': _perform_data_migration_insert,
    'update': _perform_data_migration_update,
    'delete': _perform_data_migration_delete,
}


def _perform_data_migration(model, data):
    table = _import_model(model).__table__

    for operation, rows in data.items():
        _data_migration_operations[operation](table, rows)


def _import_model(model_path):
    from ttgn.pokedex.utils import import_string

    return import_string('ttgn.pokedex.models.{}'.format(model_path))
