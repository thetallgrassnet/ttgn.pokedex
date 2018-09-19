"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import context, op
import sqlalchemy as sa
import ttgn.pokedex.utils
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade():
    if not ttgn.pokedex.utils.if_x_argument('no-schema', False):
        schema_upgrade()

    if not ttgn.pokedex.utils.if_x_argument('no-data', False):
        data_upgrade()


def downgrade():
    if not ttgn.pokedex.utils.if_x_argument('no-data', False):
        data_downgrade()

    if not ttgn.pokedex.utils.if_x_argument('no-schema', False):
        schema_downgrade()


def schema_upgrade():
    ${upgrades if upgrades else "pass"}


def schema_downgrade():
    ${downgrades if downgrades else "pass"}


def data_upgrade():
    try:
        ttgn.pokedex.utils.load_data_migration_if_exists(${repr(up_revision)}, 'upgrade')
    except Exception:
        data_downgrade()
        schema_downgrade()
        raise


def data_downgrade():
    ttgn.pokedex.utils.load_data_migration_if_exists(${repr(up_revision)}, 'downgrade')
