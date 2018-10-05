"""Generic utility functions."""


def snake_case(name):
    """Converts a CamelCase string to snake_case."""
    import re
    sub_1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', sub_1).lower()


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
