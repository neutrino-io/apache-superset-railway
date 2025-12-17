# Apache Superset on Railway

[![Deploy on Railway](https://railway.com/button.svg)](https://railway.app/template/954W6r?referralCode=cWyE73)

Production-ready Apache Superset deployment on Railway with PostgreSQL metadata database, persistent storage, and ClickHouse support.

Modified from: https://medium.com/towards-data-engineering/quick-setup-configure-superset-with-docker-a5cca3992b28

## Features

- **PostgreSQL Metadata Database** - Production-grade metadata storage
- **Persistent Volume Storage** - Data survives deployments and restarts
- **ClickHouse Support** - Pre-configured dual drivers (HTTP + Native protocol)
- **Multi-Database Support** - PostgreSQL, MySQL, MSSQL, MongoDB drivers included
- **Production Optimized** - Connection pooling, health checks, auto-restart
- **Secure by Default** - Secret key management, proper permissions
- **Environment-Based Configuration** - Easy admin user setup via environment variables

## Quick Start

### 1. Prerequisites

- Railway account
- PostgreSQL database provisioned in Railway
- Git repository connected to Railway

### 2. Configuration

All configuration is in `railway.toml`. Update these values:

```toml
[deploy.env]
ADMIN_EMAIL = "your-email@example.com"
ADMIN_USERNAME = "your-username"
ADMIN_PASSWORD = "your-secure-password"
SQLALCHEMY_DATABASE_URI = "postgresql://user:pass@host:port/database"
SECRET_KEY = "your-generated-secret-key"
SUPERSET_SECRET_KEY = "your-generated-superset-secret-key"
```

**Generate Secret Keys:**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 3. Deploy

```bash
# Connect to Railway
railway link

# Deploy
railway up
```

Or push to main branch if auto-deploy is enabled:
```bash
git push origin main
```

### 4. Access

Once deployed, access Superset at:
```
https://<your-railway-domain>.up.railway.app
```

Login with your admin credentials.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Railway Platform                    │
│                                                          │
│  ┌──────────────┐    ┌──────────────┐   ┌────────────┐ │
│  │   Superset   │───▶│  PostgreSQL  │   │  Volume    │ │
│  │  (Docker)    │    │  (Metadata)  │   │  (Storage) │ │
│  └──────────────┘    └──────────────┘   └────────────┘ │
│         │                                               │
│         │                                               │
│         ▼                                               │
│  ┌──────────────┐                                       │
│  │  ClickHouse  │  (Optional Data Source)               │
│  │  (Database)  │                                       │
│  └──────────────┘                                       │
└─────────────────────────────────────────────────────────┘
```

### Components

1. **Superset Container** - Apache Superset web application
2. **PostgreSQL** - Metadata database (stores charts, dashboards, users)
3. **Persistent Volume** - Stores uploads, cache, and logs
4. **ClickHouse** - Optional data source with native driver support

## Configuration Files

### railway.toml
Railway deployment configuration with environment variables and volume setup.

**Location:** `/Users/REDACTED_USERNAME/Projects/Neutrino/Sources/railway-superset/railway.toml`

### config/superset_config.py
Superset application configuration including database connections and security settings.

**Location:** `/Users/REDACTED_USERNAME/Projects/Neutrino/Sources/railway-superset/config/superset_config.py`

### Dockerfile
Container build instructions with all database drivers.

**Location:** `/Users/REDACTED_USERNAME/Projects/Neutrino/Sources/railway-superset/Dockerfile`

### config/superset_init.sh
Initialization script that sets up database, creates admin user, and starts Superset.

**Location:** `/Users/REDACTED_USERNAME/Projects/Neutrino/Sources/railway-superset/config/superset_init.sh`

## Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `SQLALCHEMY_DATABASE_URI` | PostgreSQL connection string | `postgresql://user:pass@host:port/db` |
| `ADMIN_USERNAME` | Admin username | `admin` |
| `ADMIN_EMAIL` | Admin email | `admin@example.com` |
| `ADMIN_PASSWORD` | Admin password | `SecurePass123!` |
| `SECRET_KEY` | Flask secret key | Generated string |
| `SUPERSET_SECRET_KEY` | Superset secret key | Generated string |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Application port | `8088` |
| `SUPERSET_ENV` | Environment | `production` |
| `DATA_DIR` | Data directory | `/app/superset_home/data` |
| `UPLOAD_FOLDER` | Upload directory | `/app/superset_home/uploads` |

See `.env.example` for complete list.

## Persistent Storage

The Railway volume at `/app/superset_home` persists:

```
/app/superset_home/
├── data/           # Application data and cache
├── uploads/        # User uploaded files
└── logs/           # Application logs
```

This ensures data survives:
- Container restarts
- New deployments
- Application updates

## Database Drivers

Pre-installed drivers for connecting to various databases:

- **PostgreSQL** - `psycopg2-binary`
- **ClickHouse** - `clickhouse-connect`, `clickhouse-driver`
- **MySQL** - `mysqlclient`
- **MSSQL** - `pymssql`, `pyodbc`
- **MongoDB** - `pymongo`

## ClickHouse Configuration

### Dual Driver Support

1. **clickhouse-connect** - HTTP protocol, high performance
2. **clickhouse-driver** - Native protocol, Railway compatible

### Connection Formats

**HTTP Protocol:**
```
clickhousedb://username:password@host:8123/database
```

**Native Protocol (Recommended for Railway):**
```
clickhouse+native://username:password@host:9000/database
```

### Adding ClickHouse Data Source

1. Go to Data → Databases
2. Click "+ Database"
3. Select "ClickHouse"
4. Enter connection details:
   - Display Name: `My ClickHouse`
   - SQLAlchemy URI: `clickhouse+native://user:pass@host:port/db`
5. Test Connection
6. Save

## Security

### Secret Keys

Generate new secret keys for production:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

Update both `SECRET_KEY` and `SUPERSET_SECRET_KEY` in `railway.toml`.

### Password Security

- Use strong passwords (mixed case, numbers, special characters)
- Change default passwords immediately
- Rotate credentials periodically

### Database Credentials

- Use Railway's secret management
- Enable SSL for database connections
- Use read-only credentials for data sources when possible

## Monitoring

### Health Checks

Railway monitors the `/health` endpoint:
- Timeout: 300 seconds
- Restart on failure: Up to 3 retries

### Logs

View logs in Railway dashboard or via CLI:

```bash
railway logs
```

### Metrics

Monitor in Railway dashboard:
- CPU usage
- Memory usage
- Network traffic
- Volume usage

## Troubleshooting

### Database Connection Failed

**Symptoms:** Error during initialization, "Database connection failed"

**Solutions:**
1. Verify `SQLALCHEMY_DATABASE_URI` is correct
2. Check PostgreSQL database is running
3. Test connection manually:
   ```bash
   railway run python3 -c "from sqlalchemy import create_engine; engine = create_engine('$SQLALCHEMY_DATABASE_URI'); engine.connect()"
   ```

### ClickHouse Not Available

**Symptoms:** ClickHouse not in database list

**Solutions:**
1. Check initialization logs for driver import errors
2. Verify drivers installed in Dockerfile
3. Check dialect registration in `config/superset_config.py`

### Volume Permission Issues

**Symptoms:** "Permission denied" on `/app/superset_home`

**Solutions:**
1. Verify Dockerfile creates directories with correct ownership
2. Check volume mount path in `railway.toml`
3. Review container logs for permission errors

### Admin User Exists

**Symptoms:** "Admin user already exists" during restart

**Note:** This is normal behavior. The initialization script handles this gracefully.

To reset admin password:
```bash
railway run superset fab reset-password --username REDACTED_USERNAME
```

## Maintenance

### Database Vacuum (Monthly)

```bash
railway run psql $DATABASE_URL -c "VACUUM ANALYZE;"
```

### Check Database Size

```bash
railway run psql $DATABASE_URL -c "SELECT pg_size_pretty(pg_database_size('superset'));"
```

### View Volume Usage

Check in Railway dashboard: Settings → Volumes → superset-data

## Upgrading

### 1. Update Base Image

Edit `Dockerfile`:
```dockerfile
FROM apache/superset:3.0.0  # Specify new version
```

### 2. Test Locally

```bash
docker build -t superset-test .
docker run -p 8088:8088 superset-test
```

### 3. Deploy

```bash
git add Dockerfile
git commit -m "Upgrade Superset to 3.0.0"
git push origin main
```

Database migrations run automatically during initialization.

## Backup and Recovery

### PostgreSQL Backup

```bash
railway run pg_dump $DATABASE_URL > backup.sql
```

### Restore from Backup

```bash
railway run psql $DATABASE_URL < backup.sql
```

### Volume Backup

Railway automatically backs up volumes. Additional backups can be configured via Railway CLI.

## Performance Optimization

### Connection Pool

Adjust in `config/superset_config.py`:

```python
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 10,
    'max_overflow': 20,
    'pool_pre_ping': True,
    'pool_recycle': 300,
}
```

### Redis Cache (Recommended)

Add Redis to Railway project, then update `railway.toml`:

```toml
REDIS_HOST = "redis.railway.internal"
REDIS_PORT = "6379"
CACHE_REDIS_URL = "redis://redis.railway.internal:6379/0"
```

Update `config/superset_config.py`:

```python
CACHE_CONFIG = {
    'CACHE_TYPE': 'RedisCache',
    'CACHE_REDIS_URL': os.environ.get('CACHE_REDIS_URL'),
}
```

## Documentation

- **Deployment Guide:** `DEPLOYMENT.md` - Comprehensive deployment documentation
- **Environment Variables:** `.env.example` - All available environment variables
- **Superset Docs:** https://superset.apache.org/docs/intro
- **Railway Docs:** https://docs.railway.app

## Project Structure

```
railway-superset/
├── config/
│   ├── superset_config.py      # Superset configuration
│   └── superset_init.sh         # Initialization script
├── clickhouse_railway_engine.py # Custom ClickHouse engine
├── Dockerfile                   # Container build instructions
├── railway.toml                 # Railway deployment config
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
├── DEPLOYMENT.md                # Detailed deployment guide
└── README.md                    # This file
```

## Support

For issues and questions:

1. Check `DEPLOYMENT.md` for detailed troubleshooting
2. Review Railway logs: `railway logs`
3. Check Superset documentation: https://superset.apache.org/docs/intro
4. Railway support: https://railway.app/help

## License

Apache Superset is licensed under the Apache License 2.0.

## Contributors

- Azri Jamil (admin@example.com)

---

**Note:** This configuration is optimized for Railway deployment. For other platforms, modifications may be required.
