import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Add the app module to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import Base  # Ensure your models are imported here

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# PostgreSQL Database Configuration
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', 5432)
DB_NAME = os.getenv('DB_NAME', 'admin_panel')
DB_USER = os.getenv('DB_USER', 'a_panel')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'backend')

# Timezone Configuration
TIMEZONE='Asia/Kathmandu'

# SQLAlchemy Configuration
SQLALCHEMY_DATABASE_URL= "postgresql+psycopg2://a_panel:backend@localhost:5432/admin_panel"	
SQLALCHEMY_TRACK_MODIFICATIONS=False

# Alembic Configuration (for migrations)
ALEMBIC_INI_PATH='alembic.ini'
ALEMBIC_SCRIPT_PATH='alembic/versions'

# Application Configuration
APP_NAME='AdminPanel'
APP_SECRET_KEY='e16e72bc7edbceb216b475fafb37a205e402eb11a1598537c276378c578e513a'
DEBUG=True

# Alembic Config object, which provides access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# Set up database URL from environment variables
config.set_main_option('sqlalchemy.url', os.getenv('SQLALCHEMY_DATABASE_URL'))

# Add your model's MetaData object here for 'autogenerate' support
target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"}
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()