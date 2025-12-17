# ClickHouse Dual Driver Setup for Superset

This repository has been configured to include both ClickHouse drivers for maximum compatibility:

- **clickhouse-connect**: Modern high-performance HTTP driver
- **clickhouse-driver**: Native protocol driver for Railway compatibility

## Installation Details

Both ClickHouse drivers have been added to the Dockerfile (`Dockerfile:18-21`):

```dockerfile
# Install both clickhouse-connect (HTTP) and clickhouse-driver (native) for compatibility
RUN pip install --no-cache-dir \
    clickhouse-connect[sqlalchemy] \
    clickhouse-driver
```

## ClickHouse Connection Configuration

### Connecting to ClickHouse in Superset

1. **Build and run the Superset container**
2. **Navigate to Superset UI** → Data → Databases
3. **Add a new database** with the following connection string format:

#### For ClickHouse Server (HTTP Protocol):
```
clickhouse+http://username:password@hostname:8123/database
```

#### For ClickHouse Server (Native Protocol):
```
clickhouse+native://username:password@hostname:9000/database
```

#### For ClickHouse Cloud:
```
clickhouse+http://username:password@hostname:8443/database?secure=true
```

#### For Railway ClickHouse (Native Protocol - REQUIRED):
```
clickhouse+native://username:password@hostname.railway.app:23230/database
```

### Connection String Parameters

- **clickhouse+http** - Uses HTTP interface (for standard ClickHouse)
- **clickhouse+native** - Uses native TCP protocol (required for Railway)
- **username** - ClickHouse username (often 'default')
- **password** - ClickHouse password
- **hostname** - ClickHouse server hostname or IP
- **port** - ClickHouse port (8123 for HTTP, 9000 for native, Railway uses 23230)
- **database** - Default database to connect to

### Example Connection Strings

- **Local ClickHouse**: `clickhouse+native://default:@localhost:9000/default`
- **Remote ClickHouse**: `clickhouse+native://admin:password123@clickhouse.example.com:9000/analytics`
- **ClickHouse Cloud**: `clickhouse+http://default:cloud_password@your-instance.clickhouse.cloud:8443/default?secure=true`
- **Railway ClickHouse**: `clickhouse+native://default:$$74qimqfukgop1ega34t2znnswagku88v@nozomi.proxy.rlwy.net:23230/default`

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