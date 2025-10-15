import os

FEATURE_FLAGS = {
    "ENABLE_TEMPLATE_PROCESSING": True,
}

PREVENT_UNSAFE_DB_CONNECTIONS = False
ENABLE_PROXY_FIX = True

# Database engine configuration for ClickHouse
SQLALCHEMY_EXAMPLES_URI = "clickhouse+connect://default:@localhost:9000/default"

SECRET_KEY = os.environ.get("SECRET_KEY")
