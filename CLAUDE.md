# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an Apache Superset deployment configured for Railway platform. It uses:
- **PostgreSQL** for metadata storage (charts, dashboards, users)
- **ClickHouse** as the primary data source (sector2.election_pahang dataset)
- **Persistent volumes** for uploads, cache, and logs
- **Docker** with custom initialization and configuration

The project includes comprehensive REST API documentation for programmatic chart creation and management.

## Key Architecture Decisions

### Dual Database Architecture
- **PostgreSQL (Metadata)**: Superset's internal database via `SQLALCHEMY_DATABASE_URI`
- **ClickHouse (Data Source)**: Connected via Superset UI using native protocol (`clickhouse+native://`)
- The metadata database stores Superset's configuration; data sources are added separately in Superset UI

### ClickHouse Driver Strategy
Two drivers are installed for maximum compatibility:
- `clickhouse-connect`: HTTP protocol (port 8123)
- `clickhouse-driver`: Native protocol (port 9000/9440) - **preferred for Railway**

Railway ClickHouse uses non-standard ports (e.g., port 23230 for native). Connection URIs must use the native protocol format with Railway-assigned ports.

### Volume Persistence Pattern
The init script (`scripts/superset_init.sh`) runs as root to create volume directories, then switches to the `superset` user. This two-phase approach solves Railway volume permission issues:
1. Root creates `/app/superset_home/{data,uploads,logs}`
2. `chown -R superset:superset /app/superset_home`
3. Switch to superset user for application runtime

### Configuration Loading Order
1. `Dockerfile` installs dependencies and sets up Python paths
2. `config/superset_config.py` configures Superset (loaded via `SUPERSET_CONFIG_PATH`)
3. `scripts/superset_init.sh` initializes database and starts application
4. `railway.toml` defines environment variables and volume mounts

## Critical Files

### scripts/superset_init.sh
Docker ENTRYPOINT that handles:
- Volume directory creation and permissions (runs as root)
- PostgreSQL connectivity testing
- Database initialization (`superset db upgrade`)
- Admin user creation (idempotent - skips if exists)
- Application startup

**Important**: This script is referenced by both Dockerfile ENTRYPOINT and railway.toml `startCommand`.

### config/superset_config.py
Main Superset configuration with:
- Dynamic Python version detection for driver compatibility
- ClickHouse dialect registration for both native and HTTP protocols
- PostgreSQL metadata database configuration
- Redis fallback logic (uses in-memory if REDIS_URL not set)
- Rate limiting configuration (currently disabled via `RATELIMIT_ENABLED = False`)

**Key pattern**: Uses `os.environ.get()` with sensible defaults for all configuration.

### railway.toml
Railway deployment configuration defining:
- Volume mount at `/app/superset_home`
- Environment variables (admin credentials, database URI, secret keys)
- Health check path (`/health`) with 300s timeout
- Restart policy (ON_FAILURE, max 3 retries)

**Security Note**: Contains actual credentials - treat as sensitive.

### Dockerfile
Multi-stage build that:
1. Detects Python version dynamically (compatibility across Superset versions)
2. Installs database drivers to `/app/.venv/lib/python3.10/site-packages`
3. Verifies all drivers during build (fail-fast approach)
4. Copies scripts from `/scripts` directory (not `/config`)
5. Stays as root user for init script requirements

## Common Development Commands

### Local Testing
```bash
# Build Docker image
docker build -t superset-test .

# Run locally (requires PostgreSQL)
docker run -p 8088:8088 \
  -e SQLALCHEMY_DATABASE_URI="postgresql://user:pass@host:5432/superset" \
  -e ADMIN_USERNAME="admin" \
  -e ADMIN_EMAIL="admin@example.com" \
  -e ADMIN_PASSWORD="password" \
  -e SECRET_KEY="your-secret-key" \
  superset-test
```

### Railway Deployment
```bash
# Link to Railway project
railway link

# Deploy current state
railway up

# View logs
railway logs

# Run commands in Railway environment
railway run bash
```

### Database Operations
```bash
# Reset admin password (in Railway)
railway run superset fab reset-password --username REDACTED_USERNAME

# Run database migrations
railway run superset db upgrade

# Access PostgreSQL metadata database
railway run psql $SQLALCHEMY_DATABASE_URI

# Backup metadata database
railway run pg_dump $SQLALCHEMY_DATABASE_URI > backup.sql
```

### Script Testing
```bash
# Verify configuration before deployment
bash scripts/verify-config.sh

# Test ClickHouse driver installation
python3 scripts/verify_clickhouse.py
```

## REST API Usage

### Authentication Pattern
All API requests require:
1. **JWT Token**: Obtained from `/api/v1/security/login`
2. **CSRF Token**: Obtained from `/api/v1/security/csrf_token/`
3. **Cookies**: Session cookies from login (critical for CSRF validation)

**Important**: Cookie management is essential. Use `curl -b cookies.txt -c cookies.txt` to persist cookies across requests.

### Chart Creation Workflow
```bash
# 1. Login and save cookies
curl -c cookies.txt -X POST "$BASE_URL/api/v1/security/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"user@example.com","password":"pass","provider":"db","refresh":true}' \
  > login.json

# 2. Extract access token
TOKEN=$(cat login.json | jq -r '.access_token')

# 3. Get CSRF token (must use cookies)
CSRF=$(curl -s -b cookies.txt -c cookies.txt \
  -H "Authorization: Bearer $TOKEN" \
  "$BASE_URL/api/v1/security/csrf_token/" | jq -r '.result')

# 4. Create chart (requires all three: token, CSRF, cookies)
curl -b cookies.txt -c cookies.txt \
  -X POST "$BASE_URL/api/v1/chart/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: $CSRF" \
  -H "Referer: $BASE_URL/" \
  -d '{"slice_name":"Chart Name","viz_type":"pie","datasource_id":1,...}'
```

### Chart JSON Structure
Charts require two stringified JSON fields:
- `params`: UI configuration (groupby, metrics, filters, colors)
- `query_context`: Query definition (datasource, filters, metrics, row_limit)

**Critical**: Both must be JSON strings within the outer JSON payload.

## Dataset Information

### ClickHouse Data Source
- **Database**: sector2.election_pahang
- **Records**: 1,048,540 voters (Pahang electoral demographics)
- **Database ID**: 16 (ClickHouse Connect)
- **Dataset ID**: 1

### Key Columns
- `parlimen`: Parliamentary constituency (14 constituencies)
- `dun`: State assembly constituency
- `daerah`: District (12 districts)
- `umur`: Age
- `agama`: Religion
- `date_lahir`: Date of birth
- Geographic: `negeri`, `bandar`, `poskod`

## Documentation Structure

All documentation is in `/docs` with this organization:
- **setup/** - Installation and driver configuration
- **deployment/** - Railway deployment guides and checklists
- **troubleshooting/** - Common issues and fixes
- **guides/** - REST API chart creation tutorial (20KB)
- **reference/** - Chart types catalog (40+ charts with decision tree)
- **api/** - Complete REST API reference

For chart creation: Start with `docs/guides/superset_chart_creation_guide.md`, reference chart types in `docs/reference/superset_chart_types_reference.md`.

## Troubleshooting Patterns

### "No module named 'psycopg2'" Error
- **Cause**: Python version mismatch or driver not in path
- **Fix**: `config/superset_config.py` dynamically detects Python version and adds to path
- **Verify**: Check driver installation in Dockerfile build logs

### "CSRF token is missing" Error
- **Cause**: Missing cookies in request
- **Fix**: Use cookie file with `-b` and `-c` flags in all requests after login
- **Verify**: Ensure CSRF request uses cookies from login

### "Empty query" Chart Error
- **Cause**: Invalid `params` or `query_context` JSON
- **Fix**: Ensure both are valid JSON strings (not objects)
- **Debug**: Check Superset logs for actual error message

### Volume Permission Errors
- **Cause**: Railway volume mounted with incorrect permissions
- **Fix**: Init script runs as root to set ownership before switching users
- **Verify**: Check init script logs for permission operations

## Secret Management

### Required Secrets
Generate with: `python3 -c "import secrets; print(secrets.token_urlsafe(32))"`

- `SECRET_KEY`: Flask session encryption
- `SUPERSET_SECRET_KEY`: Superset internal encryption
- `ADMIN_PASSWORD`: Admin user password

### Database Credentials
- **PostgreSQL URI**: Format `postgresql://user:pass@host:port/database`
- **ClickHouse URI**: Format `clickhouse+native://user:pass@host:port/database`
- **Password escaping**: Use `$$` for literal `$` in Railway environment variables

## Environment Variable Precedence

Config loading order (later overrides earlier):
1. Dockerfile ENV statements
2. railway.toml `[deploy.env]` section
3. Railway dashboard environment variables
4. `config/superset_config.py` `os.environ.get()` with defaults

## Rate Limiting Configuration

Currently **disabled** (`RATELIMIT_ENABLED = False`) to avoid Redis dependency issues on Railway.

To enable in production:
1. Deploy Redis service on Railway
2. Set `REDIS_URL` environment variable
3. Enable rate limiting: `RATELIMIT_ENABLED = True` in `config/superset_config.py`

## Chart Types Reference

**Verified Working Charts** (tested via REST API):
- `table` - Data tables with metrics
- `pie` - Percentage breakdowns
- `big_number_total` - Single KPI display
- `sunburst_v2` - Multi-level hierarchies

**Common Chart Types**:
- `echarts_timeseries_bar` - Bar charts
- `echarts_timeseries_line` - Line charts
- `histogram` - Distributions
- `deck_scatter`, `deck_heatmap` - Geographic (requires lat/lon)

See `docs/reference/superset_chart_types_reference.md` for complete catalog with decision tree.

## Access URLs

- **Superset Instance**: `https://apache-superset-railway-production-13fe.up.railway.app`
- **Chart Explorer**: `https://apache-superset-railway-production-13fe.up.railway.app/explore/?slice_id={id}`
- **API Base**: `https://apache-superset-railway-production-13fe.up.railway.app/api/v1`

## Working with ClickHouse Data

### Connecting via REST API
Always use REST API for ClickHouse queries (per user guidelines). Direct database access pattern:

```bash
# Query via ClickHouse HTTP interface
curl -u "default:$PASSWORD" \
  "https://clickhouse-host.railway.app/" \
  --data "SELECT parlimen, COUNT(*) as voters FROM sector2.election_pahang GROUP BY parlimen"
```

### Connection String Format
Railway ClickHouse credentials are in environment:
- **Host**: Railway proxy URL (e.g., `nozomi.proxy.rlwy.net`)
- **Port**: Railway-assigned (e.g., 23230 for native, varies)
- **User**: `default`
- **Password**: Contains `$` - must escape as `$$` in environment variables

## Production Recommendations

### Performance Optimization
- Add Redis for distributed caching and rate limiting
- Configure connection pooling in `SQLALCHEMY_ENGINE_OPTIONS`
- Use `row_limit` in chart queries to prevent large data transfers

### Security Hardening
- Rotate secret keys periodically
- Use read-only credentials for data sources when possible
- Enable SSL for database connections
- Configure proper CORS settings for production domains

### Monitoring
- Monitor `/health` endpoint (automated by Railway)
- Track PostgreSQL database size growth
- Monitor volume usage in Railway dashboard
- Review Superset logs for errors: `railway logs`

## Important: Always Access ClickHouse via REST

Per user requirements, always use REST API to access the ClickHouse database. Do not use direct database connection methods unless there are specific limitations that prevent REST API usage.
