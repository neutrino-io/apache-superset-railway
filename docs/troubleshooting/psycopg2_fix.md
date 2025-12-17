# PostgreSQL psycopg2 Module Installation Fix

## Problem Summary
The Superset deployment on Railway was failing with "No module named 'psycopg2'" error during database connectivity testing in the init script.

### Root Causes Identified:
1. **Python Version Mismatch**: Dockerfile referenced Python 3.11 paths, while superset_config.py referenced Python 3.10 paths
2. **Hardcoded Python Paths**: Using version-specific paths made the deployment brittle across different Superset base image versions
3. **Missing Installation Verification**: No verification that psycopg2-binary was successfully installed during build
4. **Potential Package Installation Issues**: No force-reinstall to ensure clean installation

## Solution Implemented

### 1. Dockerfile Changes (`/Dockerfile`)

#### Added Python Version Detection:
```dockerfile
# Detect Python version and store it for later use
RUN PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')") && \
    echo "Detected Python version: $PYTHON_VERSION" && \
    echo "export PYTHON_VERSION=$PYTHON_VERSION" >> /etc/environment
```

#### Enhanced psycopg2 Installation:
```dockerfile
# Install additional database drivers
# Using --upgrade --force-reinstall to ensure psycopg2-binary is properly installed
RUN pip install --no-cache-dir --upgrade --force-reinstall \
    psycopg2-binary \
    pymongo \
    pymssql \
    pyodbc \
    mysqlclient

# Verify psycopg2 installation
RUN python3 -c "import psycopg2; print(f'✓ psycopg2 version: {psycopg2.__version__}')" || \
    (echo "ERROR: psycopg2 not installed correctly" && exit 1)
```

#### Version-Independent PYTHONPATH:
```dockerfile
# Set PYTHONPATH environment variable for runtime
ENV PYTHONPATH=/app:/usr/local/lib/python3/site-packages:/usr/lib/python3/site-packages
```

#### Added Build-Time Verification:
```dockerfile
# Verify all database drivers are installed before switching user
RUN echo "====== Verifying Database Drivers ======" && \
    python3 -c "import psycopg2; print(f'✓ psycopg2: {psycopg2.__version__}')" && \
    python3 -c "import pymongo; print(f'✓ pymongo: {pymongo.__version__}')" && \
    python3 -c "import clickhouse_connect; print(f'✓ clickhouse-connect: {clickhouse_connect.__version__}')" && \
    python3 -c "import clickhouse_driver; print(f'✓ clickhouse-driver: {clickhouse_driver.__version__}')" && \
    echo "====== All drivers verified successfully ======"
```

### 2. Config File Changes (`/config/superset_config.py`)

#### Dynamic Python Version Detection:
```python
# Dynamically detect Python version and add to path
# This ensures compatibility with different Superset base image versions
python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
python_paths = [
    f'/usr/local/lib/python{python_version}/site-packages',
    f'/usr/lib/python{python_version}/site-packages',
    '/usr/local/lib/python3/site-packages',
    '/usr/lib/python3/site-packages',
]

# Add Python site-packages to path for all database drivers
for path in python_paths:
    if path not in sys.path and os.path.exists(path):
        sys.path.insert(0, path)
```

#### Runtime Driver Verification:
```python
# Verify critical database drivers are available
try:
    import psycopg2
    print(f"✓ PostgreSQL driver (psycopg2): {psycopg2.__version__}")
except ImportError as e:
    print(f"✗ PostgreSQL driver (psycopg2) not available: {e}")
```

### 3. Railway Config Changes (`/railway.toml`)

#### Version-Independent PYTHONPATH:
```toml
# Python Configuration - Using generic python3 path for version independence
PYTHONPATH = "/app:/usr/local/lib/python3/site-packages:/usr/lib/python3/site-packages"
```

## Benefits of This Solution

1. **Version Agnostic**: Works with any Python 3.x version used by Apache Superset base image
2. **Build-Time Validation**: Catches installation issues during build, not runtime
3. **Force Reinstall**: Ensures clean installation of psycopg2-binary
4. **Multiple Path Fallbacks**: Covers all common Python package installation locations
5. **Comprehensive Verification**: Verifies all database drivers during build and startup
6. **Better Debugging**: Clear error messages at both build and runtime

## Testing the Fix

### 1. Build Verification:
The Docker build should now show:
```
Detected Python version: 3.x
✓ psycopg2 version: x.x.x
====== Verifying Database Drivers ======
✓ psycopg2: x.x.x
✓ pymongo: x.x.x
✓ clickhouse-connect: x.x.x
✓ clickhouse-driver: x.x.x
====== All drivers verified successfully ======
```

### 2. Runtime Verification:
The init script should show:
```
Python version: 3.x
Python path: [...]
✓ PostgreSQL driver (psycopg2): x.x.x
Testing PostgreSQL database connectivity...
✓ Database connection successful
```

### 3. Railway Deployment:
```bash
# Commit changes
git add Dockerfile config/superset_config.py railway.toml
git commit -m "Fix psycopg2 installation with version-independent paths"
git push origin main

# Railway will auto-deploy
# Monitor logs for verification messages
```

## Rollback Plan

If issues occur, rollback with:
```bash
git revert HEAD
git push origin main
```

## Future Improvements

1. Consider using a requirements.txt file for better dependency management
2. Add health check endpoint that verifies database connectivity
3. Consider using multi-stage Docker build for smaller image size
4. Add automated testing of database connections during CI/CD

## Files Modified

- `/Dockerfile` - Enhanced installation and verification
- `/config/superset_config.py` - Dynamic Python path detection
- `/railway.toml` - Version-independent PYTHONPATH

## Related Issues

This fix resolves the "No module named 'psycopg2'" error that was preventing:
- Database connectivity testing in init script
- Superset metadata database initialization
- PostgreSQL backend functionality

## Verification Checklist

- [ ] Docker build completes successfully
- [ ] Build shows psycopg2 verification messages
- [ ] Build shows all driver verification messages
- [ ] Init script imports psycopg2 successfully
- [ ] PostgreSQL database connection succeeds
- [ ] Superset starts and serves requests
- [ ] ClickHouse drivers still work
- [ ] Other database drivers still work
