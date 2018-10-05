# pylint: disable=invalid-name
"""Language translations

Revision ID: 1888d425f419
Revises: 088903c1ed2a
Create Date: 2018-09-29 23:09:09.102410

"""
import sqlalchemy as sa
from alembic import op

from ttgn.pokedex.migrations import if_x_argument
from ttgn.pokedex.migrations.data import load_data_migrations

# revision identifiers, used by Alembic.
revision = '1888d425f419'
down_revision = '088903c1ed2a'
branch_labels = None
depends_on = None


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
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'ttgn_pokedex_models_multilang_language_translations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('language_id', sa.Integer(), nullable=False),
        sa.Column('local_language_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.Unicode(), nullable=False),
        sa.ForeignKeyConstraint(
            ['language_id'],
            ['ttgn_pokedex_models_multilang_languages.id'],
        ),
        sa.ForeignKeyConstraint(
            ['local_language_id'],
            ['ttgn_pokedex_models_multilang_languages.id'],
        ), sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('language_id', 'local_language_id'))
    # ### end Alembic commands ###


def schema_downgrade():
    """Perform schema downgrade."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ttgn_pokedex_models_multilang_language_translations')
    # ### end Alembic commands ###


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
