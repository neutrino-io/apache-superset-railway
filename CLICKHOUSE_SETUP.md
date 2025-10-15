# ClickHouse Driver Setup for Superset

This repository has been configured to include the ClickHouse driver for Apache Superset.

## Installation Details

The ClickHouse driver has been added to the Dockerfile (`Dockerfile:22`):

```dockerfile
RUN pip install \
    psycopg2-binary \
    pymongo \
    pymssql \
    pyodbc \
    mysqlclient \
    clickhouse-connect
```

## ClickHouse Connection Configuration

### Connecting to ClickHouse in Superset

1. **Build and run the Superset container**
2. **Navigate to Superset UI** → Data → Databases
3. **Add a new database** with the following connection string format:

#### For ClickHouse Server (Native Protocol):
```
clickhouse+connect://username:password@hostname:9000/database
```

#### For ClickHouse Server (HTTP Protocol):
```
clickhouse+http://username:password@hostname:8123/database
```

#### For ClickHouse Cloud:
```
clickhouse+connect://username:password@hostname:8443/database?secure=true
```

### Connection String Parameters

- **clickhouse+connect** - Uses the native ClickHouse protocol (recommended)
- **clickhouse+http** - Uses HTTP interface (alternative option)
- **username** - ClickHouse username (often 'default')
- **password** - ClickHouse password
- **hostname** - ClickHouse server hostname or IP
- **port** - ClickHouse port (9000 for native, 8123 for HTTP, 8443 for cloud)
- **database** - Default database to connect to

### Example Connection Strings

- **Local ClickHouse**: `clickhouse+connect://default:@localhost:9000/default`
- **Remote ClickHouse**: `clickhouse+connect://admin:password123@clickhouse.example.com:9000/analytics`
- **ClickHouse Cloud**: `clickhouse+connect://default:cloud_password@your-instance.clickhouse.cloud:8443/default?secure=true`

## Verification

To verify the ClickHouse driver installation, you can run:

```bash
python verify_clickhouse.py
```

This script will test if the ClickHouse driver can be imported and instantiated correctly.

## Additional Configuration

The Superset configuration has been updated in `config/superset_config.py` to include:

```python
# Database engine configuration for ClickHouse
SQLALCHEMY_EXAMPLES_URI = "clickhouse+connect://default:@localhost:9000/default"
```

This sets up the ClickHouse connection dialect for Superset to recognize.

## Features Supported

The `clickhouse-connect` driver supports:

- High-performance data transfer
- Automatic type conversion
- Connection pooling
- SSL/TLS support for ClickHouse Cloud
- NumPy and Pandas integration
- SQLAlchemy integration for Superset

## Troubleshooting

If you encounter connection issues:

1. **Check ClickHouse server is running** and accessible from the Superset container
2. **Verify network connectivity** between Superset and ClickHouse
3. **Check credentials** and ensure the user has permissions to access the database
4. **Validate the connection string format** matches your ClickHouse setup

For more information about the ClickHouse Python driver, visit:
https://github.com/ClickHouse/clickhouse-connect