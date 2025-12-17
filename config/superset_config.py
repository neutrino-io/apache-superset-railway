import os
import sys
from sqlalchemy.dialects import registry

# Dynamically detect Python version and add to path
# This ensures compatibility with different Superset base image versions
python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
python_paths = [
    f'/usr/local/lib/python{python_version}/site-packages',
    f'/usr/lib/python{python_version}/site-packages',
    '/usr/local/lib/python3/site-packages',
    '/usr/lib/python3/site-packages',
]

# Add Python site-packages to path for all database drivers
for path in python_paths:
    if path not in sys.path and os.path.exists(path):
        sys.path.insert(0, path)

print(f"Python version: {python_version}")
print(f"Python path: {sys.path[:5]}")  # Print first 5 paths

# Verify critical database drivers are available
try:
    import psycopg2
    print(f"✓ PostgreSQL driver (psycopg2): {psycopg2.__version__}")
except ImportError as e:
    print(f"✗ PostgreSQL driver (psycopg2) not available: {e}")

# Add ClickHouse modules to Python path
try:
    import clickhouse_connect
    print(f"✓ ClickHouse Connect version: {clickhouse_connect.__version__}")
except ImportError as e:
    print(f"Warning: ClickHouse Connect not available: {e}")

try:
    import clickhouse_driver
    print(f"✓ ClickHouse Driver version: {clickhouse_driver.__version__}")
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

# ============================================================================
# PostgreSQL Configuration - Superset Metadata Database
# ============================================================================
# Configure PostgreSQL as the metadata database (replaces default SQLite)
# This is where Superset stores its internal metadata, user info, charts, dashboards, etc.
SQLALCHEMY_DATABASE_URI = os.environ.get(
    'SQLALCHEMY_DATABASE_URI',
    'sqlite:////app/superset_home/superset.db'  # Fallback to SQLite if env var not set
)

# Use SUPERSET_SECRET_KEY as primary, fall back to SECRET_KEY
SECRET_KEY = os.environ.get("SUPERSET_SECRET_KEY") or os.environ.get("SECRET_KEY")

# Additional Superset security configuration
if not SECRET_KEY:
    print("WARNING: No SECRET_KEY or SUPERSET_SECRET_KEY set. Using insecure default.")
    SECRET_KEY = "CHANGE_ME_TO_A_RANDOM_SECRET_KEY"

FEATURE_FLAGS = {
    "ENABLE_TEMPLATE_PROCESSING": True,
}

PREVENT_UNSAFE_DB_CONNECTIONS = False
ENABLE_PROXY_FIX = True

# ============================================================================
# ClickHouse Configuration
# ============================================================================
# Database engine configuration for ClickHouse
# Use native protocol for Railway compatibility
SQLALCHEMY_EXAMPLES_URI = "clickhouse+native://default:@localhost:9000/default"

# Additional ClickHouse configuration
CLICKHOUSE_HTTP_PORT = 8123
CLICKHOUSE_NATIVE_PORT = 9000

# ============================================================================
# SQLAlchemy Engine Configuration
# ============================================================================
# Enable detailed logging for database connections
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
    'echo': False,
}

# ============================================================================
# Data Persistence Configuration
# ============================================================================
# Configure data directories for volume mounting
DATA_DIR = '/app/superset_home/data'
UPLOAD_FOLDER = '/app/superset_home/uploads'

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ============================================================================
# Helper Functions
# ============================================================================
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

# ============================================================================
# Production Configuration
# ============================================================================
# Additional production settings
SUPERSET_WEBSERVER_TIMEOUT = 300
ROW_LIMIT = 50000

# Cache configuration (optional, can be enhanced with Redis)
CACHE_CONFIG = {
    'CACHE_TYPE': 'SimpleCache',
    'CACHE_DEFAULT_TIMEOUT': 300
}

# Print configuration summary
print("=" * 70)
print("Superset Configuration Summary")
print("=" * 70)
print(f"Python Version: {python_version}")
print(f"Metadata Database: {SQLALCHEMY_DATABASE_URI.split('@')[0] if '@' in SQLALCHEMY_DATABASE_URI else 'SQLite'}")
print(f"Data Directory: {DATA_DIR}")
print(f"Upload Directory: {UPLOAD_FOLDER}")
print(f"ClickHouse Support: Enabled (Native Protocol)")
print("=" * 70)
