import os
import alembic

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
ALEMBIC_INI_PATH=alembic.ini
ALEMBIC_SCRIPT_PATH='alembic/versions'

# Application Configuration
APP_NAME='AdminPanel'
APP_SECRET_KEY='e16e72bc7edbceb216b475fafb37a205e402eb11a1598537c276378c578e513a'
DEBUG=True