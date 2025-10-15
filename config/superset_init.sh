#!/bin/bash

# Wait for the application to fully initialize
sleep 5

# Import ClickHouse Connect modules
python3 -c "
import sys
print('Python path:', sys.path)
try:
    import clickhouse_connect
    print('✓ ClickHouse Connect imported successfully')
    print('  Version:', clickhouse_connect.__version__)
    print('  Features: High-performance HTTP driver with SQLAlchemy support')
except ImportError as e:
    print('✗ ClickHouse Connect import failed:', e)

try:
    from sqlalchemy import create_engine
    print('✓ SQLAlchemy imported successfully')
except ImportError as e:
    print('✗ SQLAlchemy import failed:', e)

try:
    # Test clickhouse-connect SQLAlchemy integration
    from clickhouse_connect.driver import create_engine as ch_create_engine
    print('✓ ClickHouse Connect SQLAlchemy integration available')
except ImportError as e:
    print('✗ ClickHouse Connect SQLAlchemy integration failed:', e)
"

# create Admin user, you can read these values from env or anywhere else possible
superset fab create-admin --username "$ADMIN_USERNAME" --firstname Superset --lastname Admin --email "$ADMIN_EMAIL" --password "$ADMIN_PASSWORD"

# Upgrading Superset metastore
superset db upgrade

# setup roles and permissions
superset superset init

# Load example data (optional)
superset load-examples

# Starting server
/bin/sh -c /usr/bin/run-server.sh