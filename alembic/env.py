import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# 1. Підтягуємо глобальні налаштування Alembic
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 2. Імпортуємо наш базовий клас моделей та самі моделі
from app.db.session import Base
from app.db.base import * # Цей імпорт підтягне всі 5 моделей для міграції

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Запуск міграцій в offline режимі."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    """Запуск міграцій в асинхронному online режимі."""
    import os
    from app.core.config import settings
    
    # Спочатку перевіряємо, чи є змінна в системному оточенні контейнера,
    # якщо немає — беремо дефолт із pydantic settings
    database_url = os.getenv("DATABASE_URL", settings.DATABASE_URL)
    
    configuration = config.get_section(config.config_ini_section) or {}
    configuration["sqlalchemy.url"] = database_url

    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())