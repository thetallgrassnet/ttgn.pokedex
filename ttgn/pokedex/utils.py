def snake_case(name):
    import re
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def if_x_argument(arg, default):
    from alembic import context
    return context.get_x_argument(as_dictionary=True).get(arg, default)


def load_data_migration_if_exists(rev, direction):
    if not direction in ['upgrade', 'downgrade']:
        raise RuntimeError('Invalid data migration direction')

    import pathlib
    import ttgn.pokedex

    data_path = pathlib.Path(ttgn.pokedex.base_path, 'ttgn', 'pokedex',
                             'migrations', 'data')
    data_migrations = data_path.glob('{}_{}_*.csv'.format(rev, direction))

    for file in data_migrations:
        import csv
        import re

        data = {'insert': [], 'update': [], 'delete': []}
        model = re.match(r'{}_{}_(.*)\.csv'.format(rev, direction),
                         file.name).group(1)

        with file.open(newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if not 'id' in row:
                    raise KeyError('id')

                operation = row.pop('_operation')
                if not operation in data:
                    raise RuntimeError('Invalid data operation')

                data[operation].append(row)

        if data['insert']:
            from alembic.op import bulk_insert

            table = import_model(model).__table__
            bulk_insert(table, data['insert'])

        if data['update']:
            from alembic.op import execute
            from sqlalchemy.sql.expression import bindparam

            table = import_model(model).__table__
            stmt = table.update().where(table.c.id == bindparam('id')).values({
                key: bindparam(key)
                for key in data['update'][0].keys() if not key == 'id'
            })

            execute(stmt, data['update'])

        if data['delete']:
            from alembic.op import execute
            from sqlalchemy.sql.expression import bindparam

            table = import_model(model).__table__
            stmt = table.delete().where(table.c.id == bindparam('id'))

            execute(stmt, data['delete'])


def import_model(model_path):
    return import_string('ttgn.pokedex.models.{}'.format(model_path))


def import_string(dotted_path):
    """Import a dotted module path and return the entity designated by the last
    name in the path."""
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError:
        raise ImportError(
            '{} doesn\'t look like a module path'.format(dotted_path))

    import importlib
    module = importlib.import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError:
        raise ImportError('Module {} has no class or attribute {}'.format(
            module_path, class_name))
