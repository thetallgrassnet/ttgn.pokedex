"""Utility methods for Alembic migrations."""
from alembic import context


def if_x_argument(arg, default):
    """Evaluates if a given x argument was passed to Alembic, using the given
    default if not."""
    return context.get_x_argument(as_dictionary=True).get(arg, default)
