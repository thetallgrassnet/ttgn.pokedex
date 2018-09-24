"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
import sqlalchemy as sa
from alembic import context, op
from ttgn.pokedex.migrations.data import if_x_argument, load_data_migrations
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade():
    if not if_x_argument('no-schema', False):
        schema_upgrade()

    if not if_x_argument('no-data', False):
        data_upgrade()


def downgrade():
    if not if_x_argument('no-data', False):
        data_downgrade()

    if not if_x_argument('no-schema', False):
        schema_downgrade()


def schema_upgrade():
    ${upgrades if upgrades else "pass"}


def schema_downgrade():
    ${downgrades if downgrades else "pass"}


def data_upgrade():
    try:
        load_data_migrations(revision, 'upgrade')
    except Exception:
        data_downgrade()
        schema_downgrade()
        raise


def data_downgrade():
    load_data_migrations(revision, 'downgrade')
