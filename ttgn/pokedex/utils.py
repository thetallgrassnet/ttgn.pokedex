"""Generic utility functions."""


def snake_case(name):
    """Converts a CamelCase string to snake_case.

    Parameters
    ----------
    name : str

    Returns
    -------
    str

    """
    import re
    sub_1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', sub_1).lower()


def import_string(dotted_path):
    """Import a module by its fully-qualified Python path and return the
    entity designated by the last name in the path.

    Parameters
    ----------
    dotted_path : str
        The fully-qualified path to an entity, e.g. ``package.module.attr``.

    Returns
    -------
    object

    Raises
    ------
    ImportError
        If a malformed module path, or a module path that doesn't resolve to
        an importable entity, is passed as `dotted_path`.

    """
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
