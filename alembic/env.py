from logging.config import fileConfig

from alembic import context
from sensym_db_api.sensym_models.voice_analysis_db import voice_db_models, base, db_engine

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = base.Base.metadata
# target_metadata = None

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

user, password, host, port, database, schema = db_engine.get_db_creds()


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """

    url = f"postgresql://{user}:{password}@{host}:{port}/postgres"
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        include_schemas=True,
        version_table_schema=schema,
    )

    with context.begin_transaction():
        context.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")
        context.execute(f"SET search_path TO {schema}")
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = db_engine.create_db_engine()

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata,
            include_schemas=True,
            version_table_schema=schema,
        )

        with context.begin_transaction():
            context.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")
            context.execute(f"SET search_path TO {schema}")
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
