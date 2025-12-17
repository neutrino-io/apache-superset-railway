#!/bin/bash
set -e

echo "======================================================================"
echo "Superset Initialization Starting"
echo "======================================================================"

# Create data directories if they don't exist (needed for volume mounting)
# Running as root to handle volume permissions
echo "Ensuring data directories exist with correct permissions..."
mkdir -p /app/superset_home/data
mkdir -p /app/superset_home/uploads
mkdir -p /app/superset_home/logs
chown -R superset:superset /app/superset_home
echo "✓ Data directories ready with superset user ownership"

# Wait for the application to fully initialize
echo "Waiting for application initialization..."
sleep 5

# Test database connectivity
echo "Testing PostgreSQL database connectivity..."
python3 -c "
import os
import sys
from sqlalchemy import create_engine, text

db_uri = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:////app/superset_home/superset.db')
print(f'Database URI: {db_uri.split(\"@\")[0] if \"@\" in db_uri else \"SQLite\"}')

try:
    engine = create_engine(db_uri)
    with engine.connect() as conn:
        result = conn.execute(text('SELECT 1'))
        print('✓ Database connection successful')
except Exception as e:
    print(f'✗ Database connection failed: {e}')
    sys.exit(1)
" || {
    echo "ERROR: Database connection failed. Please check your SQLALCHEMY_DATABASE_URI"
    exit 1
}

# Import ClickHouse modules (both HTTP and Native drivers)
echo "======================================================================"
echo "Testing ClickHouse Driver Support"
echo "======================================================================"
python3 -c "
import sys
print('Python path:', sys.path)
try:
    import clickhouse_connect
    print('✓ ClickHouse Connect (HTTP) imported successfully')
    print('  Version:', clickhouse_connect.__version__)
    print('  Features: High-performance HTTP driver with SQLAlchemy support')
except ImportError as e:
    print('✗ ClickHouse Connect import failed:', e)

try:
    import clickhouse_driver
    print('✓ ClickHouse Driver (Native) imported successfully')
    print('  Version:', clickhouse_driver.__version__)
    print('  Features: Native protocol support for Railway compatibility')
except ImportError as e:
    print('✗ ClickHouse Driver import failed:', e)

try:
    from sqlalchemy import create_engine
    print('✓ SQLAlchemy imported successfully')
except ImportError as e:
    print('✗ SQLAlchemy import failed:', e)

try:
    from sqlalchemy.dialects import registry
    registry.register('clickhouse', 'clickhouse_driver.dbapi.extras.dialect', 'ClickHouseDialect')
    registry.register('clickhouse+native', 'clickhouse_driver.dbapi.extras.dialect', 'ClickHouseDialect')
    print('✓ ClickHouse native dialects registered successfully')
except Exception as e:
    print('✗ Dialect registration failed:', e)

try:
    from PIL import Image
    import PIL
    print(f'✓ Pillow (PIL) version {PIL.__version__} - Screenshot and PDF generation enabled')
except ImportError as e:
    print('✗ Pillow (PIL) not available:', e)
"

echo "======================================================================"
echo "Superset Database Initialization"
echo "======================================================================"

# Run all Superset commands as superset user (we created dirs as root above)
echo "Switching to superset user for database operations..."

# Upgrade the database schema
echo "Upgrading Superset metadata database..."
su -s /bin/bash superset -c "superset db upgrade" || {
    echo "ERROR: Database upgrade failed"
    exit 1
}

# Create admin user
echo "Creating admin user..."
su -s /bin/bash superset -c "superset fab create-admin \
    --username '$ADMIN_USERNAME' \
    --firstname Superset \
    --lastname Admin \
    --email '$ADMIN_EMAIL' \
    --password '$ADMIN_PASSWORD'" || {
    echo "Note: Admin user may already exist (this is normal on restart)"
}

# Initialize roles and permissions
echo "Initializing roles and permissions..."
su -s /bin/bash superset -c "superset init" || {
    echo "ERROR: Superset initialization failed"
    exit 1
}

# Load example data is DISABLED for production
# Uncomment the following lines if you want to load example datasets for testing
# echo "Loading example data..."
# superset load-examples || {
#     echo "Note: Example data loading failed or already loaded (this is normal)"
# }
echo "Skipping example data loading (disabled for production)"

echo "======================================================================"
echo "Superset Initialization Complete"
echo "======================================================================"
echo "Configuration:"
echo "  - Admin Username: $ADMIN_USERNAME"
echo "  - Admin Email: $ADMIN_EMAIL"
echo "  - Database: PostgreSQL"
echo "  - ClickHouse Support: Enabled"
echo "  - Pillow (PIL): Enabled for screenshots and PDFs"
echo "  - Data Directory: /app/superset_home"
echo "  - Example Data: Disabled (production mode)"
echo "======================================================================"
echo "Starting Superset web server..."
echo "======================================================================"
echo "FLASK_APP is set to: $FLASK_APP"
echo "======================================================================"

# Start the server as superset user
exec su -s /bin/bash superset -c "/usr/bin/run-server.sh"
