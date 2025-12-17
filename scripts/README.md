# Scripts Directory

Utility and initialization scripts for Railway Superset deployment.

## 📁 Scripts Overview

### Initialization Scripts

**superset_init.sh** *(5.3KB)*
- **Purpose**: Main initialization script for Superset deployment
- **Usage**: Automatically executed by Docker ENTRYPOINT
- **Functions**:
  - Creates data directories with correct permissions
  - Tests PostgreSQL database connectivity
  - Initializes Superset database schema
  - Creates admin user if not exists
  - Starts Superset application server
- **Called by**: Dockerfile ENTRYPOINT and railway.toml startCommand
- **Runs as**: root (switches to superset user after directory setup)

### Database Integration Scripts

**clickhouse_railway_engine.py** *(6.0KB)*
- **Purpose**: Custom ClickHouse engine for Railway compatibility
- **Usage**: Referenced by Superset configuration for ClickHouse connections
- **Functions**:
  - Provides custom SQLAlchemy engine for ClickHouse
  - Bypasses ClickHouse dialect issues on Railway
  - Uses clickhouse-driver directly for connections
- **Called by**: Copied to /app/ by Dockerfile, used by superset_config.py

### Verification & Testing Scripts

**verify-config.sh** *(10KB)*
- **Purpose**: Configuration verification utility
- **Usage**: `bash scripts/verify-config.sh`
- **Functions**:
  - Verifies all configuration files are properly set up
  - Checks environment variables
  - Validates file permissions
  - Tests configuration syntax
  - Color-coded output for pass/fail status
- **When to use**: Before deployment, after configuration changes

**verify_clickhouse.py** *(1.2KB)*
- **Purpose**: ClickHouse driver installation verification
- **Usage**: `python3 scripts/verify_clickhouse.py`
- **Functions**:
  - Tests if clickhouse-connect can be imported
  - Verifies driver version
  - Tests basic driver functionality
  - Confirms SQLAlchemy integration
- **When to use**: After installing ClickHouse drivers, troubleshooting connections

## 🚀 Usage Examples

### Run Initialization Script (Automatic)
```bash
# Automatically called by Docker
# No manual execution needed - runs on container start
```

### Verify Configuration
```bash
# Run before deployment
cd /Users/REDACTED_USERNAME/Projects/Neutrino/Sources/railway-superset
bash scripts/verify-config.sh
```

### Test ClickHouse Driver
```bash
# Test ClickHouse installation
python3 scripts/verify_clickhouse.py
```

### Use Custom ClickHouse Engine
```python
# In superset_config.py or Python code
from clickhouse_railway_engine import ClickHouseRailwayEngine

engine = ClickHouseRailwayEngine("clickhouse+native://user:pass@host:9440/db")
```

## 📋 Script Dependencies

### superset_init.sh
- **System**: bash, chown, mkdir
- **Python**: python3, sqlalchemy
- **Environment Variables**:
  - SQLALCHEMY_DATABASE_URI (PostgreSQL connection)
  - ADMIN_USERNAME, ADMIN_EMAIL, ADMIN_PASSWORD
  - SUPERSET_CONFIG_PATH

### clickhouse_railway_engine.py
- **Python Packages**:
  - sqlalchemy
  - clickhouse-driver
  - logging (stdlib)

### verify-config.sh
- **System**: bash, grep, test
- **Files**: Checks railway.toml, Dockerfile, config files

### verify_clickhouse.py
- **Python Packages**:
  - clickhouse-connect
  - clickhouse-driver
  - sqlalchemy

## 🔧 Maintenance Notes

### Updating Scripts

1. **superset_init.sh**: Critical deployment script
   - Test changes in development environment first
   - Ensure volume permissions are correctly set
   - Verify database migration steps work
   - Update Dockerfile if path changes

2. **clickhouse_railway_engine.py**: Database integration
   - Test with actual ClickHouse instance
   - Verify SQLAlchemy compatibility
   - Update superset_config.py if interface changes

3. **Verification scripts**: Safe to modify
   - Update checks as configuration evolves
   - Add new verification steps as needed
   - Keep output user-friendly

### Adding New Scripts

When adding new scripts to this folder:

1. Add descriptive header comments
2. Make shell scripts executable: `chmod +x script.sh`
3. Update this README with script documentation
4. If used by Docker, update Dockerfile COPY commands
5. Test in development environment before deploying

## 📝 Related Documentation

- [Deployment Guide](../docs/deployment/deployment_guide.md)
- [ClickHouse Setup](../docs/setup/clickhouse_setup.md)
- [Troubleshooting](../docs/troubleshooting/psycopg2_fix.md)
- [Quick Start](../docs/QUICKSTART.md)

## 🔗 Referenced By

### Dockerfile
```dockerfile
COPY /scripts/superset_init.sh ./superset_init.sh
COPY /scripts/clickhouse_railway_engine.py /app/
ENTRYPOINT ["./superset_init.sh"]
```

### railway.toml
```toml
startCommand = "./superset_init.sh"
```

### config/superset_config.py
```python
# May reference clickhouse_railway_engine.py for custom connections
```

---

**Last Updated**: 2025-12-17
**Total Scripts**: 4 files (22.5KB)
**Status**: Production-ready
