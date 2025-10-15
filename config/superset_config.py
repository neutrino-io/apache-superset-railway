import os
import sys
from sqlalchemy.dialects import registry

# Add ClickHouse modules to Python path
try:
    import clickhouse_driver
    import clickhouse_sqlalchemy
    print(f"ClickHouse driver version: {clickhouse_driver.__version__}")
    print(f"ClickHouse SQLAlchemy version: {clickhouse_sqlalchemy.__version__}")
except ImportError as e:
    print(f"Warning: ClickHouse modules not available: {e}")

# Register ClickHouse dialect with proper error handling
try:
    registry.register('clickhouse', 'clickhouse_driver.dbapi.extras.dialect', 'ClickHouseDialect')
    print("Successfully registered ClickHouse dialect")
except Exception as e:
    print(f"Warning: Failed to register ClickHouse dialect: {e}")

# Additional dialect registration for different connection methods
try:
    registry.register('clickhouse+native', 'clickhouse_driver.dbapi.extras.dialect', 'ClickHouseDialect')
    registry.register('clickhouse+http', 'clickhouse_driver.dbapi.extras.dialect', 'ClickHouseDialect')
    print("Successfully registered ClickHouse dialect variants")
except Exception as e:
    print(f"Warning: Failed to register ClickHouse dialect variants: {e}")

FEATURE_FLAGS = {
    "ENABLE_TEMPLATE_PROCESSING": True,
}

PREVENT_UNSAFE_DB_CONNECTIONS = False
ENABLE_PROXY_FIX = True

# Database engine configuration for ClickHouse
SQLALCHEMY_EXAMPLES_URI = "clickhouse+native://default:@localhost:9000/default"

# Additional ClickHouse configuration
CLICKHOUSE_DEFAULT_PORT = 9000
CLICKHOUSE_HTTP_PORT = 8123

# Enable detailed logging for database connections
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
    'echo': False,
}

SECRET_KEY = os.environ.get("SECRET_KEY")

# Custom database engine validation
def validate_clickhouse_connection(uri):
    """Validate ClickHouse connection string format"""
    try:
        from sqlalchemy import create_engine
        engine = create_engine(uri)
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            return True
    except Exception as e:
        print(f"ClickHouse connection validation failed: {e}")
        return False

# Railway ClickHouse connection helper
def get_railway_clickhouse_uri():
    """Generate proper ClickHouse URI for Railway"""
    host = "nozomi.proxy.rlwy.net"
    port = 23230
    username = "default"
    password = "$74qimqfukgop1ega34t2znnswagku88v"
    database = "default"

    # Properly escape the password
    password = password.replace('$', '$$')

    return f"clickhouse+native://{username}:{password}@{host}:{port}/{database}"

# Export the Railway URI for easy access
RAILWAY_CLICKHOUSE_URI = get_railway_clickhouse_uri()