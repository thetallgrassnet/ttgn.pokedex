def if_x_argument(arg, default):
    from alembic import context
    return context.get_x_argument(as_dictionary=True).get(arg, default)


def load_data_migrations(rev, direction):
    import pathlib
    from ttgn.pokedex import base_path

    data_path = pathlib.Path(base_path, 'ttgn', 'pokedex', 'migrations',
                             'data')
    data_migrations = data_path.glob('{}_{}_*.csv'.format(rev, direction))
    data = _read_data_from_migrations(data_migrations)

    for model in data:
        _perform_data_migration(model, data[model])


def _read_data_from_migrations(data_migrations):
    data = {}

    for file in data_migrations:
        import csv
        import re

        match = re.match(
            r'[0-9a-f]{12}_(?:up|down)grade_'
            r'(insert|update|delete)_'
            r'([a-z_]+\.[A-Z][A-Za-z]+).*\.csv', file.name)
        operation = match.group(1)
        model = match.group(2)

        data.setdefault(model, {})[operation] = []

        with file.open(newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data[model][operation].append(row)

    return data


def _perform_data_migration_insert(table, rows):
    from alembic.op import bulk_insert
    bulk_insert(table, rows)


def _perform_data_migration_update(table, rows):
    from itertools import groupby

    from alembic.op import execute
    from sqlalchemy.sql.expression import bindparam

    for keys, rows_ in groupby(rows, key=lambda r: r.keys()):
        stmt = table.update().where(table.c.id == bindparam('id')).values(
            {key: bindparam(key)
             for key in keys if not key == 'id'})
        execute(stmt, rows)


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
