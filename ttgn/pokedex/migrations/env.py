"""Alembic migration environment configuration."""
from __future__ import with_statement

from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from ttgn.pokedex import models

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
CONFIG = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(CONFIG.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
TARGET_METADATA = models.base.Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = context.get_x_argument(as_dictionary=True).get(
        'sqlalchemy.url', None)

    if url:
        context.configure(
            url=url,
            target_metadata=TARGET_METADATA,
            literal_binds=True,
            render_as_batch=True)

        with context.begin_transaction():
            context.run_migrations()
    else:
        raise RuntimeError(
            'No database URL provided, pass one with -x sqlalchemy.url=')


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = CONFIG.attributes.get('connectable', None)

    if connectable is None:
        ini_section = CONFIG.get_section(CONFIG.config_ini_section)

        sqlalchemy_url = context.get_x_argument(as_dictionary=True).get(
            'sqlalchemy.url', None)

        if sqlalchemy_url:
            ini_section['sqlalchemy.url'] = sqlalchemy_url

            connectable = engine_from_config(
                ini_section, prefix='sqlalchemy.', poolclass=pool.NullPool)
        else:
            raise RuntimeError(
                'No database URL provided, pass one with -x sqlalchemy.url=')

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=TARGET_METADATA,
            render_as_batch=True)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
