import os
import sys
from sqlalchemy.dialects import registry

# Add system Python site-packages to path for ClickHouse modules
sys.path.insert(0, '/usr/local/lib/python3.10/site-packages')

# Add ClickHouse modules to Python path
try:
    import clickhouse_connect
    print(f"ClickHouse Connect version: {clickhouse_connect.__version__}")
except ImportError as e:
    print(f"Warning: ClickHouse Connect not available: {e}")

try:
    import clickhouse_driver
    print(f"ClickHouse Driver version: {clickhouse_driver.__version__}")
except ImportError as e:
    print(f"Warning: ClickHouse Driver not available: {e}")

# Register ClickHouse dialect with proper error handling
# Use clickhouse-driver for native protocol (Railway), clickhouse-connect for HTTP
try:
    from sqlalchemy.dialects import registry
    # Register native protocol dialect for Railway compatibility
    registry.register('clickhouse', 'clickhouse_driver.dbapi.extras.dialect', 'ClickHouseDialect')
    registry.register('clickhouse+native', 'clickhouse_driver.dbapi.extras.dialect', 'ClickHouseDialect')
    print("✅ ClickHouse native dialect registered successfully")
except Exception as e:
    print(f"Warning: Failed to register ClickHouse native dialect: {e}")

# Register HTTP dialect for clickhouse-connect
try:
    # The clickhouse-connect package registers its own HTTP dialect
    print("✅ ClickHouse Connect HTTP dialect available")
except Exception as e:
    print(f"Warning: Failed to register ClickHouse Connect dialect: {e}")

FEATURE_FLAGS = {
    "ENABLE_TEMPLATE_PROCESSING": True,
}

PREVENT_UNSAFE_DB_CONNECTIONS = False
ENABLE_PROXY_FIX = True

# Database engine configuration for ClickHouse
# Use native protocol for Railway compatibility
SQLALCHEMY_EXAMPLES_URI = "clickhouse+native://default:@localhost:9000/default"

# Additional ClickHouse configuration
CLICKHOUSE_HTTP_PORT = 8123
CLICKHOUSE_NATIVE_PORT = 9000

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
    """Generate proper ClickHouse URI for Railway using native protocol"""
    host = "nozomi.proxy.rlwy.net"
    port = 23230  # Railway ClickHouse native protocol port
    username = "default"
    password = "$74qimqfukgop1ega34t2znnswagku88v"
    database = "default"

    # Properly escape the password for environment variables
    password = password.replace('$', '$$')

    # Railway uses native protocol on port 23230
    return f"clickhouse+native://{username}:{password}@{host}:{port}/{database}"

# Export the Railway URI for easy access
RAILWAY_CLICKHOUSE_URI = get_railway_clickhouse_uri()