FROM apache/superset:latest

USER root

# Install system dependencies
RUN apt-get update && apt-get install -y \
    pkg-config \
    libmariadb-dev \
    unixodbc \
    unixodbc-dev \
    libpq-dev \
    gcc \
    g++ \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Detect Python version and store it for later use
RUN PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')") && \
    echo "Detected Python version: $PYTHON_VERSION" && \
    echo "export PYTHON_VERSION=$PYTHON_VERSION" >> /etc/environment

# Install Python dependencies to the virtual environment
# The Superset base image uses a venv at /app/.venv/lib/python3.10/site-packages
# Install both clickhouse-connect (HTTP) and clickhouse-driver (native) for compatibility
RUN /usr/local/bin/pip install --no-cache-dir \
    --target=/app/.venv/lib/python3.10/site-packages \
    clickhouse-connect[sqlalchemy] \
    clickhouse-driver

# Install additional database drivers to the venv
RUN /usr/local/bin/pip install --no-cache-dir \
    --target=/app/.venv/lib/python3.10/site-packages \
    psycopg2-binary \
    pymongo \
    pymssql \
    pyodbc \
    mysqlclient

# Install Pillow for screenshot and PDF generation features
# This enables dashboard exports, reports, and thumbnails
RUN /usr/local/bin/pip install --no-cache-dir \
    --target=/app/.venv/lib/python3.10/site-packages \
    pillow

# Verify psycopg2 installation
RUN python3 -c "import psycopg2; print(f'✓ psycopg2 version: {psycopg2.__version__}')"

# Verify Pillow installation
RUN python3 -c "from PIL import Image; import PIL; print(f'✓ Pillow version: {PIL.__version__}')"

# Create persistent data directories
# These will be mounted as volumes in Railway
RUN mkdir -p /app/superset_home/data && \
    mkdir -p /app/superset_home/uploads && \
    mkdir -p /app/superset_home/logs && \
    chown -R superset:superset /app/superset_home

# Environment variables
ENV ADMIN_USERNAME=$ADMIN_USERNAME
ENV ADMIN_EMAIL=$ADMIN_EMAIL
ENV ADMIN_PASSWORD=$ADMIN_PASSWORD

# Copy configuration files
COPY /config/superset_init.sh ./superset_init.sh
RUN chmod +x ./superset_init.sh

COPY /config/superset_config.py /app/
COPY clickhouse_railway_engine.py /app/

# Configure Superset paths and application
ENV SUPERSET_CONFIG_PATH=/app/superset_config.py
ENV SECRET_KEY=$SECRET_KEY
ENV SUPERSET_HOME=/app/superset_home
ENV FLASK_APP=superset.app:create_app()

# Set Python path dynamically based on detected Python version
# This ensures all installed packages are available
RUN PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')") && \
    echo "export PYTHONPATH=/app:/usr/local/lib/python${PYTHON_VERSION}/site-packages:/usr/lib/python${PYTHON_VERSION}/site-packages:\$PYTHONPATH" >> /etc/profile.d/python_path.sh && \
    chmod +x /etc/profile.d/python_path.sh

# Set PYTHONPATH environment variable for runtime
ENV PYTHONPATH=/app:/usr/local/lib/python3/site-packages:/usr/lib/python3/site-packages

# Verify all database drivers are installed before switching user
RUN echo "====== Verifying Database Drivers ======" && \
    python3 -c "import psycopg2; print(f'✓ psycopg2: {psycopg2.__version__}')" && \
    python3 -c "import pymongo; print(f'✓ pymongo: {pymongo.__version__}')" && \
    python3 -c "import clickhouse_connect; print(f'✓ clickhouse-connect: {clickhouse_connect.__version__}')" && \
    python3 -c "import clickhouse_driver; print(f'✓ clickhouse-driver: {clickhouse_driver.__version__}')" && \
    python3 -c "from PIL import Image; import PIL; print(f'✓ Pillow: {PIL.__version__}')" && \
    echo "====== All drivers verified successfully ======"

# Note: Staying as root to allow init script to create volume directories
# Init script will switch to superset user after directory setup
# USER superset

# Expose port (Railway will map this automatically)
EXPOSE 8088

ENTRYPOINT ["./superset_init.sh"]
