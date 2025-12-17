# Deployment Checklist - Railway Superset with PostgreSQL

Use this checklist to ensure a successful deployment of Apache Superset on Railway with PostgreSQL and persistent storage.

## Pre-Deployment Checklist

### 1. Railway Prerequisites

- [ ] Railway account created
- [ ] Railway CLI installed (optional, but recommended)
- [ ] Git repository connected to Railway project
- [ ] PostgreSQL database provisioned in Railway

### 2. Database Configuration

- [ ] PostgreSQL connection string obtained from Railway
- [ ] Connection string format verified: `postgresql://user:pass@host:port/database`
- [ ] Database name is `superset` (or updated accordingly)
- [ ] Database is accessible from Railway services

### 3. Security Configuration

- [ ] Generated new SECRET_KEY:
  ```bash
  python3 -c "import secrets; print(secrets.token_urlsafe(32))"
  ```
  Result: `_______________________________`

- [ ] Generated new SUPERSET_SECRET_KEY:
  ```bash
  python3 -c "import secrets; print(secrets.token_urlsafe(32))"
  ```
  Result: `_______________________________`

- [ ] Created strong admin password (mixed case, numbers, special characters)
- [ ] Admin email is valid and accessible
- [ ] Admin username chosen (avoid "admin" for security)

### 4. Configuration Files

- [ ] `railway.toml` created with all environment variables
- [ ] `SQLALCHEMY_DATABASE_URI` updated in railway.toml
- [ ] `ADMIN_USERNAME` updated in railway.toml
- [ ] `ADMIN_EMAIL` updated in railway.toml
- [ ] `ADMIN_PASSWORD` updated in railway.toml
- [ ] `SECRET_KEY` updated in railway.toml
- [ ] `SUPERSET_SECRET_KEY` updated in railway.toml
- [ ] Volume configuration verified in railway.toml

### 5. File Verification

Run the verification script:
```bash
chmod +x verify-config.sh
./verify-config.sh
```

- [ ] All required files present
- [ ] No critical errors in verification
- [ ] Warnings reviewed and addressed

### 6. Git Repository

- [ ] `.gitignore` file created
- [ ] `.env` file NOT committed (if exists)
- [ ] All configuration files added to git
- [ ] Changes committed with descriptive message

## Deployment Steps

### Step 1: Update Configuration

```bash
# Edit railway.toml with your values
nano railway.toml
```

Update these values:
```toml
ADMIN_EMAIL = "YOUR-EMAIL@example.com"
ADMIN_USERNAME = "YOUR-USERNAME"
ADMIN_PASSWORD = "YOUR-SECURE-PASSWORD"
SQLALCHEMY_DATABASE_URI = "postgresql://user:pass@host:port/superset"
SECRET_KEY = "YOUR-GENERATED-SECRET-KEY-1"
SUPERSET_SECRET_KEY = "YOUR-GENERATED-SECRET-KEY-2"
```

- [ ] Configuration updated

### Step 2: Commit Changes

```bash
git add .
git commit -m "Configure PostgreSQL and persistent storage for Superset"
```

- [ ] Changes committed

### Step 3: Deploy to Railway

**Option A: Push to main branch (if auto-deploy enabled)**
```bash
git push origin main
```

**Option B: Use Railway CLI**
```bash
railway link  # If not already linked
railway up
```

- [ ] Deployment initiated

### Step 4: Monitor Deployment

In Railway dashboard:
1. Go to your Superset service
2. Click on "Deployments"
3. Watch the build logs

Look for:
- [ ] Build completes successfully
- [ ] "Testing PostgreSQL database connectivity"
- [ ] "✓ Database connection successful"
- [ ] "✓ ClickHouse Connect (HTTP) imported successfully"
- [ ] "✓ ClickHouse Driver (Native) imported successfully"
- [ ] "Upgrading Superset metadata database..."
- [ ] "Creating admin user..."
- [ ] "Initializing roles and permissions..."
- [ ] "Superset Initialization Complete"
- [ ] "Starting Superset web server..."
- [ ] Health check passing

### Step 5: Access Superset

1. In Railway dashboard, find your service URL
2. Click the URL or copy it
3. Access Superset in browser

- [ ] Superset UI loads successfully
- [ ] Login page appears

### Step 6: Login and Verify

Login with your admin credentials:
- Username: (from ADMIN_USERNAME)
- Password: (from ADMIN_PASSWORD)

- [ ] Successfully logged in
- [ ] Dashboard loads
- [ ] No error messages

## Post-Deployment Verification

### 1. Database Connection

Go to: **Settings → Database Connections**

- [ ] Can view database connections
- [ ] PostgreSQL metadata database is working (no errors)

### 2. ClickHouse Support

Go to: **Data → Databases → + Database**

- [ ] "ClickHouse" appears in database list
- [ ] Can select ClickHouse option
- [ ] Connection form appears

### 3. Create Test Chart

1. Go to **Charts**
2. Click **+ Chart**
3. Select a dataset
4. Create a simple chart
5. Save the chart

- [ ] Chart created successfully
- [ ] Chart saved
- [ ] Chart appears in chart list

### 4. Restart Test

In Railway dashboard:
1. Go to your Superset service
2. Click "Restart"
3. Wait for restart to complete

After restart:
- [ ] Service comes back online
- [ ] Can login again
- [ ] Previous charts still exist
- [ ] Data persists (volume working)

### 5. Volume Verification

Check Railway dashboard:
1. Go to **Settings → Volumes**
2. Find "superset-data" volume

- [ ] Volume is mounted
- [ ] Volume shows usage
- [ ] Volume path is `/app/superset_home`

### 6. Logs Review

Check logs for any errors:
```bash
railway logs
```

- [ ] No critical errors
- [ ] Database migrations successful
- [ ] No connection failures
- [ ] ClickHouse drivers loaded

## Security Hardening (Post-Deployment)

### 1. Change Admin Password

In Superset:
1. Go to **Settings → User Info & Security**
2. Click on your user
3. Change password

- [ ] Admin password changed from default

### 2. Review Permissions

- [ ] Review default roles
- [ ] Adjust permissions as needed
- [ ] Create additional users if needed

### 3. Configure HTTPS

- [ ] Verify Railway provides HTTPS (automatic)
- [ ] All connections use HTTPS

### 4. Enable Additional Security

In `config/superset_config.py`, consider adding:
```python
# Force HTTPS
ENABLE_PROXY_FIX = True

# Session configuration
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# CSRF protection
WTF_CSRF_ENABLED = True
```

- [ ] Security settings reviewed
- [ ] Additional security configured (if needed)

## Optional: Add ClickHouse Data Source

### 1. Prepare ClickHouse Connection

Get your ClickHouse connection details:
- Host: `nozomi.proxy.rlwy.net`
- Port: `23230` (native) or `8123` (HTTP)
- Username: `default`
- Password: Your ClickHouse password
- Database: `default`

- [ ] ClickHouse connection details ready

### 2. Add Database in Superset

1. Go to **Data → Databases**
2. Click **+ Database**
3. Select **ClickHouse**
4. Enter connection details:
   - Display Name: `My ClickHouse`
   - SQLAlchemy URI: `clickhouse+native://user:pass@host:port/database`
5. Click **Test Connection**
6. Click **Save**

- [ ] ClickHouse database added
- [ ] Connection test successful
- [ ] Database saved

### 3. Create ClickHouse Chart

1. Go to **Data → Datasets**
2. Click **+ Dataset**
3. Select your ClickHouse database
4. Select a table
5. Create dataset
6. Create chart from dataset

- [ ] Dataset created from ClickHouse
- [ ] Chart created successfully

## Optional: Performance Optimization

### 1. Add Redis Cache

In Railway:
1. Add Redis service
2. Note Redis connection URL

Update `railway.toml`:
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

- [ ] Redis added (optional)
- [ ] Cache configured

### 2. Adjust Connection Pool

In `config/superset_config.py`:
```python
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 10,
    'max_overflow': 20,
    'pool_pre_ping': True,
    'pool_recycle': 300,
}
```

- [ ] Connection pool optimized (if needed)

## Monitoring Setup

### 1. Railway Monitoring

In Railway dashboard:
- [ ] CPU usage monitored
- [ ] Memory usage monitored
- [ ] Deployment logs reviewed
- [ ] Health checks passing

### 2. Superset Logs

- [ ] Log volume created and mounted
- [ ] Logs accessible via Railway
- [ ] No recurring errors

### 3. Database Monitoring

- [ ] PostgreSQL metrics available
- [ ] Database size monitored
- [ ] Connection count monitored

## Backup Strategy

### 1. PostgreSQL Backup

Set up automated backups:
```bash
# Manual backup
railway run pg_dump $DATABASE_URL > backup.sql
```

- [ ] Backup strategy defined
- [ ] Regular backups scheduled

### 2. Volume Backup

- [ ] Railway volume auto-backup enabled
- [ ] Additional backup configured (optional)

## Documentation

- [ ] Deployment details documented
- [ ] Admin credentials stored securely (password manager)
- [ ] Team members notified
- [ ] Access instructions shared

## Troubleshooting Reference

If issues occur, refer to:
- [ ] `DEPLOYMENT.md` - Detailed deployment guide
- [ ] `QUICKSTART.md` - Quick reference
- [ ] `README.md` - General documentation
- [ ] Railway logs - `railway logs`

## Success Criteria

Your deployment is successful when:

- [x] Superset is accessible via Railway URL
- [x] Can login with admin credentials
- [x] PostgreSQL metadata database is working
- [x] ClickHouse drivers are available
- [x] Can create and save charts
- [x] Data persists after restart
- [x] Volume is properly mounted
- [x] Health checks are passing
- [x] No critical errors in logs
- [x] All security settings configured

## Next Steps

After successful deployment:

1. **Customize Superset**
   - [ ] Add your organization's branding
   - [ ] Configure email settings
   - [ ] Set up authentication (OAuth, LDAP, etc.)

2. **Add Data Sources**
   - [ ] Connect to production databases
   - [ ] Create datasets
   - [ ] Build dashboards

3. **User Management**
   - [ ] Create user accounts
   - [ ] Assign roles
   - [ ] Configure permissions

4. **Maintenance**
   - [ ] Schedule regular backups
   - [ ] Monitor resource usage
   - [ ] Plan for scaling

## Support Resources

- **Documentation:** `DEPLOYMENT.md`, `README.md`, `QUICKSTART.md`
- **Verification:** Run `./verify-config.sh`
- **Logs:** `railway logs`
- **Superset Docs:** https://superset.apache.org/docs/intro
- **Railway Docs:** https://docs.railway.app

---

**Deployment Date:** _______________
**Deployed By:** _______________
**Railway Project:** _______________
**Superset URL:** _______________
