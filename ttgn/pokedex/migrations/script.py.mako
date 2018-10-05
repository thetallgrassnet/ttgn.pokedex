# pylint: disable=invalid-name
"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
import sqlalchemy as sa
from alembic import op

from ttgn.pokedex.migrations import if_x_argument
from ttgn.pokedex.migrations.data import load_data_migrations
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade():
    """Perform upgrade migration."""
    if not if_x_argument('no-schema', False):
        schema_upgrade()

    if not if_x_argument('no-data', False):
        data_upgrade()


def downgrade():
    """Perform downgrade migration."""
    if not if_x_argument('no-data', False):
        data_downgrade()

    if not if_x_argument('no-schema', False):
        schema_downgrade()


def schema_upgrade():
    """Perform schema upgrade."""
    ${upgrades if upgrades else "pass"}


def schema_downgrade():
    """Perform schema downgrade."""
    ${downgrades if downgrades else "pass"}


def data_upgrade():
    """Perform data upgrade."""
    try:
        load_data_migrations(revision, 'upgrade')
    except Exception:
        data_downgrade()
        schema_downgrade()
        raise


def data_downgrade():
    """Perform data downgrade."""
    load_data_migrations(revision, 'downgrade')
