import os
from sqlalchemy.dialects import registry

# Register ClickHouse dialect explicitly
registry.register('clickhouse', 'clickhouse_driver.dbapi.extras.dialect', 'ClickHouseDialect')

FEATURE_FLAGS = {
    "ENABLE_TEMPLATE_PROCESSING": True,
}

PREVENT_UNSAFE_DB_CONNECTIONS = False
ENABLE_PROXY_FIX = True

# Database engine configuration for ClickHouse
SQLALCHEMY_EXAMPLES_URI = "clickhouse+native://default:@localhost:9000/default"

SECRET_KEY = os.environ.get("SECRET_KEY")
