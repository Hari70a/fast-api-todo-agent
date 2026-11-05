import os
from logging.config import fileConfig

from dotenv import load_dotenv
from sqlalchemy import engine_from_config, URL
from sqlalchemy import pool

from alembic import context

from database.db_engine import Base
#Important to add these models(though unused) so that alembic understands the existing schemas
from database.db_models.users import Users
from database.db_models.todos import Todos
from database.db_models.conversations import Conversations
from database.db_models.user_memories import UserMemories

load_dotenv()
# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

config.set_main_option(
    "sqlalchemy.url",
    os.getenv("DATABASE_URL")
)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
# if config.config_file_name is not None:
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
print("Base:", Base)
print("Metadata:", Base.metadata)
print("Tables:", list(Base.metadata.tables.keys()))
target_metadata = Base.metadata

print("SQLAlchemy tables:")
for table in target_metadata.sorted_tables:
    print(" -", table.fullname)

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_schemas=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        print("Alembic connected to:", connection.engine.url)
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=True
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
