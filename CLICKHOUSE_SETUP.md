# ClickHouse Connect Driver Setup for Superset

This repository has been configured to include the ClickHouse Connect driver for Apache Superset.

## Installation Details

The ClickHouse Connect driver has been added to the Dockerfile (`Dockerfile:19-20`):

```dockerfile
# Install clickhouse-connect (modern high-performance driver)
RUN pip install --no-cache-dir \
    clickhouse-connect[sqlalchemy]
```

## ClickHouse Connection Configuration

### Connecting to ClickHouse in Superset

1. **Build and run the Superset container**
2. **Navigate to Superset UI** → Data → Databases
3. **Add a new database** with the following connection string format:

#### For ClickHouse Server (HTTP Protocol - Recommended for clickhouse-connect):
```
clickhouse+http://username:password@hostname:8123/database
```

#### For ClickHouse Cloud:
```
clickhouse+http://username:password@hostname:8443/database?secure=true
```

#### For Railway ClickHouse:
```
clickhouse+http://username:password@hostname.railway.app:port/database
```

### Connection String Parameters

- **clickhouse+http** - Uses HTTP interface (recommended for clickhouse-connect)
- **username** - ClickHouse username (often 'default')
- **password** - ClickHouse password
- **hostname** - ClickHouse server hostname or IP
- **port** - ClickHouse HTTP port (8123 default, Railway uses custom ports)
- **database** - Default database to connect to

### Example Connection Strings

- **Local ClickHouse**: `clickhouse+http://default:@localhost:8123/default`
- **Remote ClickHouse**: `clickhouse+http://admin:password123@clickhouse.example.com:8123/analytics`
- **ClickHouse Cloud**: `clickhouse+http://default:cloud_password@your-instance.clickhouse.cloud:8443/default?secure=true`
- **Railway ClickHouse**: `clickhouse+http://default:password@hostname.railway.app:23230/default`

## Verification

To verify the ClickHouse driver installation, you can run:

```bash
python verify_clickhouse.py
```

This script will test if the ClickHouse driver can be imported and instantiated correctly.

## Additional Configuration

The Superset configuration has been updated in `config/superset_config.py` to include:

```python
import clickhouse_connect

# Database engine configuration for ClickHouse (HTTP interface)
SQLALCHEMY_EXAMPLES_URI = "clickhouse+http://default:@localhost:8123/default"
```

The `clickhouse-connect` package automatically registers its SQLAlchemy dialect and provides built-in integration with Superset.

## Features Supported

The `clickhouse-connect` supports:

- **High-performance HTTP driver** with maximum compatibility
- **Built-in SQLAlchemy support** for Superset integration
- **Pandas DataFrames, NumPy Arrays, PyArrow Tables** integration
- **Asyncio support** for async operations
- **Lightweight SQLAlchemy Core** (select, joins, deletes)
- **Connection pooling** and automatic type conversion
- **SSL/TLS support** for ClickHouse Cloud
- **Python 3.9+** support with modern features
- **Better reliability** through HTTP interface

## Troubleshooting

If you encounter connection issues:

1. **Check ClickHouse server is running** and accessible from the Superset container
2. **Verify network connectivity** between Superset and ClickHouse
3. **Check credentials** and ensure the user has permissions to access the database
4. **Validate the connection string format** matches your ClickHouse setup

For more information about the ClickHouse Python driver, visit:
https://github.com/ClickHouse/clickhouse-connect