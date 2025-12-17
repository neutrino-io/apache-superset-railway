# Apache Superset Railway Deployment Guide

This guide explains how to deploy Apache Superset on Railway with PostgreSQL metadata database and persistent storage.

## Architecture Overview

### Components

1. **Apache Superset** - Business Intelligence web application
2. **PostgreSQL Database** - Stores Superset metadata (charts, dashboards, users, permissions)
3. **Persistent Volume** - Stores uploaded files, cached data, and logs
4. **ClickHouse Support** - Pre-configured drivers for connecting to ClickHouse data sources

### Data Flow

```
User → Superset (Docker) → PostgreSQL (Metadata)
                          → ClickHouse (Data Sources)
                          → Volume (Uploads/Cache)
```

## Prerequisites

1. Railway account with active project
2. PostgreSQL database provisioned in Railway
3. ClickHouse database provisioned in Railway (optional, for data sources)

## Configuration Files

### 1. railway.toml
Main Railway configuration file that defines:
- Build settings (Docker)
- Deployment settings (health checks, restart policy)
- Volume mounting configuration
- Environment variables

**Location:** `/Users/REDACTED_USERNAME/Projects/Neutrino/Sources/railway-superset/railway.toml`

### 2. superset_config.py
Superset application configuration:
- PostgreSQL metadata database connection
- ClickHouse dialect registration
- Security settings
- Persistent storage directories
- Production optimizations

**Location:** `/Users/REDACTED_USERNAME/Projects/Neutrino/Sources/railway-superset/config/superset_config.py`

### 3. Dockerfile
Container configuration:
- Base image: apache/superset:latest
- Database drivers (PostgreSQL, ClickHouse, MySQL, MSSQL, MongoDB)
- Volume mount points
- User permissions

**Location:** `/Users/REDACTED_USERNAME/Projects/Neutrino/Sources/railway-superset/Dockerfile`

### 4. superset_init.sh
Initialization script that runs on container start:
- Database connectivity tests
- Database schema migrations
- Admin user creation
- Role and permission setup
- Example data loading (optional)

**Location:** `/Users/REDACTED_USERNAME/Projects/Neutrino/Sources/railway-superset/config/superset_init.sh`

## Deployment Steps

### Step 1: Railway PostgreSQL Setup

1. Create a PostgreSQL database in Railway
2. Note the connection details:
   ```
   Host: tramway.proxy.rlwy.net
   Port: 14849
   Database: superset
   Username: postgres
   Password: REDACTED_DB_PASSWORD
   ```

3. Connection string format:
   ```
   postgresql://postgres:REDACTED_DB_PASSWORD@db-host:5432/superset
   ```

### Step 2: Configure Environment Variables

The `railway.toml` file contains all required environment variables. Verify these settings:

#### Admin Credentials
```toml
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "REDACTED_PASSWORD"
ADMIN_USERNAME = "REDACTED_USERNAME"
```

#### Security Keys
```toml
SECRET_KEY = "REDACTED_SECRET_KEY"
SUPERSET_SECRET_KEY = "REDACTED_SUPERSET_SECRET_KEY"
```

**Important:** For production, generate new secret keys:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

#### Database Configuration
```toml
SQLALCHEMY_DATABASE_URI = "postgresql://postgres:REDACTED_DB_PASSWORD@db-host:5432/superset"
```

### Step 3: Configure Persistent Storage

The volume configuration in `railway.toml`:

```toml
[[deploy.volumes]]
mountPath = "/app/superset_home"
name = "superset-data"
```

This volume persists:
- `/app/superset_home/data` - Application data
- `/app/superset_home/uploads` - User uploaded files
- `/app/superset_home/logs` - Application logs

### Step 4: Deploy to Railway

1. **Connect Repository to Railway**
   ```bash
   railway link
   ```

2. **Deploy**
   ```bash
   railway up
   ```

   Or push to main branch (if auto-deploy is enabled):
   ```bash
   git add .
   git commit -m "Configure PostgreSQL and persistent storage"
   git push origin main
   ```

3. **Monitor Deployment**
   - Check Railway dashboard for build logs
   - Watch for initialization messages
   - Verify database migrations complete successfully

### Step 5: Verify Deployment

1. **Access Superset**
   - URL: `https://<your-railway-domain>.up.railway.app`
   - Login with admin credentials

2. **Check Database Connection**
   - Initialization logs should show: "✓ Database connection successful"
   - PostgreSQL should be listed as the metadata database

3. **Verify ClickHouse Support**
   - Go to Data → Databases
   - Click "+ Database"
   - Select "ClickHouse" from supported databases
   - Should see both HTTP and Native protocol options

## Database Configuration Details

### PostgreSQL Metadata Database

**Purpose:** Stores all Superset internal data
- User accounts and permissions
- Charts and dashboards
- Query history
- Saved queries
- Alerts and reports

**Configuration in superset_config.py:**
```python
SQLALCHEMY_DATABASE_URI = os.environ.get(
    'SQLALCHEMY_DATABASE_URI',
    'sqlite:////app/superset_home/superset.db'  # Fallback
)
```

**Connection Parameters:**
```python
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_pre_ping': True,      # Verify connections before use
    'pool_recycle': 300,        # Recycle connections every 5 minutes
    'echo': False,              # Disable SQL query logging
}
```

### ClickHouse Data Source Support

**Drivers Installed:**
1. `clickhouse-connect` - HTTP protocol, high performance
2. `clickhouse-driver` - Native protocol, Railway compatible

**Dialect Registration:**
```python
registry.register('clickhouse', 'clickhouse_driver.dbapi.extras.dialect', 'ClickHouseDialect')
registry.register('clickhouse+native', 'clickhouse_driver.dbapi.extras.dialect', 'ClickHouseDialect')
```

**Connection String Format:**
```
clickhouse+native://username:password@host:port/database
```

**Example Railway ClickHouse Connection:**
```
clickhouse+native://default:$74qimqfukgop1ega34t2znnswagku88v@nozomi.proxy.rlwy.net:23230/default
```

## Persistent Storage Details

### Volume Structure

```
/app/superset_home/
├── data/           # Application data and cache
├── uploads/        # User uploaded files (CSV, Excel, etc.)
└── logs/           # Application logs
```

### Data Persistence

The Railway volume ensures:
- Data survives container restarts
- Deployments don't lose user uploads
- Cache persists across restarts
- Logs are retained for debugging

### Backup Recommendations

1. **PostgreSQL Database**
   - Use Railway's automatic backups
   - Or set up pg_dump cron jobs

2. **Volume Data**
   - Railway automatically backs up volumes
   - Additional backups can be configured via Railway CLI

## Troubleshooting

### Database Connection Issues

**Error:** "Database connection failed"

**Solution:**
1. Verify SQLALCHEMY_DATABASE_URI is correct
2. Check PostgreSQL database is running
3. Verify network connectivity
4. Check credentials are correct

**Test Connection:**
```bash
railway run python3 -c "
from sqlalchemy import create_engine, text
import os
engine = create_engine(os.environ['SQLALCHEMY_DATABASE_URI'])
with engine.connect() as conn:
    print(conn.execute(text('SELECT 1')).fetchone())
"
```

### ClickHouse Connection Issues

**Error:** "ClickHouse dialect not found"

**Solution:**
1. Verify drivers are installed in Dockerfile
2. Check dialect registration in superset_config.py
3. Review initialization logs for import errors

**Test ClickHouse:**
```bash
railway run python3 -c "
import clickhouse_connect
import clickhouse_driver
print('ClickHouse drivers available')
"
```

### Volume Mounting Issues

**Error:** "Permission denied" on /app/superset_home

**Solution:**
1. Verify Dockerfile creates directories with correct permissions
2. Check volume mount path matches configuration
3. Ensure superset user owns the directories

**Verify Permissions:**
```bash
railway run ls -la /app/superset_home
```

### Initialization Script Failures

**Error:** "Database upgrade failed"

**Solution:**
1. Check PostgreSQL database is accessible
2. Verify database is empty or has compatible schema
3. Review migration logs in Railway console

**Manual Database Upgrade:**
```bash
railway run superset db upgrade
```

### Admin User Creation Fails

**Error:** "Admin user already exists"

**Note:** This is normal on restarts. The script handles this gracefully.

**Reset Admin Password:**
```bash
railway run superset fab reset-password --username REDACTED_USERNAME
```

## Security Best Practices

### 1. Secret Keys

**Generate Strong Keys:**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

Update in `railway.toml`:
```toml
SECRET_KEY = "<generated-key-1>"
SUPERSET_SECRET_KEY = "<generated-key-2>"
```

### 2. Database Credentials

- Use Railway's secret management
- Rotate credentials periodically
- Use read-only credentials for data sources when possible

### 3. Admin Password

- Change default password immediately after deployment
- Use strong password with mixed characters
- Enable 2FA if available

### 4. Network Security

- Use Railway's private networking for database connections
- Enable SSL/TLS for all connections
- Configure proper CORS settings if needed

## Performance Optimization

### 1. Database Connection Pool

Current settings in `superset_config.py`:
```python
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
    'echo': False,
}
```

For high traffic, adjust:
```python
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 10,
    'max_overflow': 20,
    'pool_pre_ping': True,
    'pool_recycle': 300,
}
```

### 2. Cache Configuration

**Current:** SimpleCache (in-memory)

**Recommended for Production:** Redis

Add to `railway.toml`:
```toml
REDIS_HOST = "redis.railway.internal"
REDIS_PORT = "6379"
CACHE_REDIS_URL = "redis://redis.railway.internal:6379/0"
```

Update `superset_config.py`:
```python
CACHE_CONFIG = {
    'CACHE_TYPE': 'RedisCache',
    'CACHE_REDIS_URL': os.environ.get('CACHE_REDIS_URL'),
    'CACHE_DEFAULT_TIMEOUT': 300
}
```

### 3. Query Result Backend

For large query results, configure async query execution:

```python
RESULTS_BACKEND = {
    'CACHE_TYPE': 'RedisCache',
    'CACHE_REDIS_URL': os.environ.get('CACHE_REDIS_URL'),
}
```

## Monitoring and Maintenance

### 1. Health Checks

Railway automatically monitors the health endpoint:
```toml
healthcheckPath = "/health"
healthcheckTimeout = 300
```

### 2. Logs

View logs via Railway CLI:
```bash
railway logs
```

Or in Railway dashboard: Deployments → Logs

### 3. Database Maintenance

**Vacuum PostgreSQL (monthly):**
```bash
railway run psql $DATABASE_URL -c "VACUUM ANALYZE;"
```

**Check Database Size:**
```bash
railway run psql $DATABASE_URL -c "
SELECT pg_size_pretty(pg_database_size('superset'));
"
```

### 4. Volume Usage

Monitor volume usage in Railway dashboard:
- Settings → Volumes → superset-data

## Upgrading Superset

### 1. Update Dockerfile

Change base image version:
```dockerfile
FROM apache/superset:3.0.0  # Specify version
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

### 4. Run Migrations

Migrations run automatically via `superset_init.sh`

## Rollback Procedure

### 1. Railway Rollback

In Railway dashboard:
1. Go to Deployments
2. Select previous successful deployment
3. Click "Redeploy"

### 2. Database Rollback

If schema migration fails:
```bash
# Restore from backup
railway run psql $DATABASE_URL < backup.sql
```

## Support and Resources

- **Superset Documentation:** https://superset.apache.org/docs/intro
- **Railway Documentation:** https://docs.railway.app
- **GitHub Issues:** https://github.com/apache/superset/issues

## File Reference

All configuration files are located in:
- Main directory: `/Users/REDACTED_USERNAME/Projects/Neutrino/Sources/railway-superset/`
- Config directory: `/Users/REDACTED_USERNAME/Projects/Neutrino/Sources/railway-superset/config/`

Key files:
- `railway.toml` - Railway deployment configuration
- `Dockerfile` - Container build instructions
- `config/superset_config.py` - Superset application configuration
- `config/superset_init.sh` - Initialization script
- `.env.example` - Environment variables template
- `DEPLOYMENT.md` - This file
