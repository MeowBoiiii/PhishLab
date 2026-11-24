from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Import konfiguracji aplikacji, klasy bazowej SQLAlchemy oraz modeli
from app.core.config import settings
from app.core.database import Base
import app.models  # noqa: F401 - wymusza załadowanie wszystkich modeli do Base.metadata

# Pobranie obiektu konfiguracyjnego z pliku alembic.ini
config = context.config

# Dynamiczne wstrzyknięcie adresu bazy z ustawień aplikacji (zamiast wpisywać hasło w alembic.ini)
config.set_main_option("sqlalchemy.url", settings.sync_database_url)

# Inicjalizacja logowania na podstawie pliku alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadane modeli SQLAlchemy - potrzebne np. do automatycznego generowania migracji (--autogenerate)
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Uruchamia migracje w trybie offline (generuje czysty SQL bez łączenia z bazą)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Uruchamia migracje w trybie online (łączy się z PostgreSQL i wprowadza zmiany)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


# Wybór trybu uruchomienia migracji
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()