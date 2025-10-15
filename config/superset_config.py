import os
import sys
from sqlalchemy.dialects import registry

# Add ClickHouse modules to Python path
try:
    import clickhouse_connect
    print(f"ClickHouse Connect version: {clickhouse_connect.__version__}")
except ImportError as e:
    print(f"Warning: ClickHouse Connect not available: {e}")

# Register ClickHouse dialect with proper error handling
# Note: clickhouse-connect has built-in SQLAlchemy support
try:
    # The clickhouse-connect package registers its own dialect
    print("ClickHouse Connect SQLAlchemy support available")
except Exception as e:
    print(f"Warning: Failed to register ClickHouse Connect dialect: {e}")

FEATURE_FLAGS = {
    "ENABLE_TEMPLATE_PROCESSING": True,
}

PREVENT_UNSAFE_DB_CONNECTIONS = False
ENABLE_PROXY_FIX = True

# Database engine configuration for ClickHouse
# Note: clickhouse-connect uses HTTP interface (port 8123) by default
SQLALCHEMY_EXAMPLES_URI = "clickhouse+http://default:@localhost:8123/default"

# Additional ClickHouse configuration
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
    """Generate proper ClickHouse URI for Railway using clickhouse-connect"""
    host = "nozomi.proxy.rlwy.net"
    port = 23230  # Railway ClickHouse HTTP port
    username = "default"
    password = "$74qimqfukgop1ega34t2znnswagku88v"
    database = "default"

    # Properly escape the password for environment variables
    password = password.replace('$', '$$')

    # clickhouse-connect uses HTTP interface by default
    return f"clickhouse+http://{username}:{password}@{host}:{port}/{database}"

# Export the Railway URI for easy access
RAILWAY_CLICKHOUSE_URI = get_railway_clickhouse_uri()