# Quick Start Guide - Railway Superset Deployment

This is a condensed guide to get Superset running on Railway quickly. For detailed documentation, see `DEPLOYMENT.md`.

## Prerequisites

- Railway account
- PostgreSQL database in Railway
- Git repository

## 5-Minute Setup

### 1. Update railway.toml

Edit `/Users/REDACTED_USERNAME/Projects/Neutrino/Sources/railway-superset/railway.toml`:

```toml
[deploy.env]
# Update these values:
ADMIN_EMAIL = "your-email@example.com"
ADMIN_USERNAME = "your-username"
ADMIN_PASSWORD = "your-password"
SQLALCHEMY_DATABASE_URI = "postgresql://user:pass@host:port/superset"
```

### 2. Generate Secret Keys

```bash
# Generate two secret keys
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

Update in `railway.toml`:
```toml
SECRET_KEY = "<first-generated-key>"
SUPERSET_SECRET_KEY = "<second-generated-key>"
```

### 3. Deploy

```bash
# Link to Railway (if not already linked)
railway link

# Deploy
railway up
```

Or push to main branch:
```bash
git add .
git commit -m "Configure PostgreSQL and persistent storage"
git push origin main
```

### 4. Access Superset

1. Go to Railway dashboard
2. Find your Superset deployment
3. Click on the generated URL
4. Login with your admin credentials

## Configuration Summary

### What's Configured

- **Metadata Database**: PostgreSQL (stores charts, dashboards, users)
- **Persistent Storage**: Volume at `/app/superset_home` (survives restarts)
- **ClickHouse Support**: Both HTTP and Native drivers pre-installed
- **Security**: Secret key management, proper permissions
- **Auto-restart**: On failure, up to 3 retries
- **Health Checks**: Monitors `/health` endpoint

### File Changes Made

1. **railway.toml** - Railway deployment configuration
   - Environment variables
   - Volume mounting
   - Health checks

2. **config/superset_config.py** - Superset configuration
   - PostgreSQL connection
   - ClickHouse dialect registration
   - Security settings
   - Persistent directories

3. **Dockerfile** - Container configuration
   - Volume support
   - Directory permissions
   - Database drivers

4. **config/superset_init.sh** - Initialization script
   - Database connectivity tests
   - Schema migrations
   - Admin user creation

## Adding ClickHouse Data Source

Once Superset is running:

1. Login to Superset
2. Go to **Data → Databases**
3. Click **+ Database**
4. Select **ClickHouse**
5. Enter connection details:
   ```
   Display Name: My ClickHouse
   SQLAlchemy URI: clickhouse+native://user:pass@host:port/database
   ```
6. Click **Test Connection**
7. Click **Save**

## Environment Variables Reference

### Required
- `SQLALCHEMY_DATABASE_URI` - PostgreSQL connection
- `ADMIN_USERNAME` - Admin username
- `ADMIN_EMAIL` - Admin email
- `ADMIN_PASSWORD` - Admin password
- `SECRET_KEY` - Flask secret
- `SUPERSET_SECRET_KEY` - Superset secret

### Optional
- `PORT` - Application port (default: 8088)
- `SUPERSET_ENV` - Environment (default: production)
- `DATA_DIR` - Data directory
- `UPLOAD_FOLDER` - Upload directory

See `.env.example` for complete list.

## Verification Checklist

After deployment, verify:

- [ ] Superset is accessible at Railway URL
- [ ] Can login with admin credentials
- [ ] PostgreSQL connection is working
- [ ] ClickHouse is available in database list
- [ ] Can create and save a chart
- [ ] Data persists after restart

## Common Issues

### Can't Access Superset

**Check:**
1. Deployment is running in Railway dashboard
2. Health check is passing
3. No build/deploy errors in logs

**Fix:**
```bash
railway logs
```

### Database Connection Failed

**Check:**
1. `SQLALCHEMY_DATABASE_URI` is correct
2. PostgreSQL database is running
3. Network connectivity

**Test:**
```bash
railway run python3 -c "from sqlalchemy import create_engine; import os; create_engine(os.environ['SQLALCHEMY_DATABASE_URI']).connect()"
```

### ClickHouse Not Available

**Check:**
1. Initialization logs for driver errors
2. Dialect registration

**Test:**
```bash
railway run python3 -c "import clickhouse_connect, clickhouse_driver; print('OK')"
```

## Next Steps

1. **Secure Your Deployment**
   - Change default passwords
   - Rotate secret keys
   - Review security settings

2. **Add Data Sources**
   - Connect to ClickHouse
   - Add other databases
   - Configure permissions

3. **Create Content**
   - Build charts
   - Create dashboards
   - Set up alerts

4. **Optimize Performance**
   - Add Redis cache
   - Adjust connection pool
   - Monitor resource usage

## Support

- **Detailed Guide:** `DEPLOYMENT.md`
- **Environment Variables:** `.env.example`
- **Superset Docs:** https://superset.apache.org/docs/intro
- **Railway Docs:** https://docs.railway.app

## File Locations

All files are in `/Users/REDACTED_USERNAME/Projects/Neutrino/Sources/railway-superset/`:

- `railway.toml` - Railway config
- `config/superset_config.py` - Superset config
- `Dockerfile` - Container config
- `config/superset_init.sh` - Init script
- `.env.example` - Environment template
- `README.md` - Full README
- `DEPLOYMENT.md` - Detailed deployment guide
- `QUICKSTART.md` - This file
