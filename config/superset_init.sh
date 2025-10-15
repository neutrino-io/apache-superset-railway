#!/bin/bash

# Wait for the application to fully initialize
sleep 5

# Import ClickHouse modules (both HTTP and Native drivers)
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