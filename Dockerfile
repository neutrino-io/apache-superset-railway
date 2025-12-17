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

# Install Python dependencies in the correct order
# Install both clickhouse-connect (HTTP) and clickhouse-driver (native) for compatibility
RUN pip install --no-cache-dir \
    clickhouse-connect[sqlalchemy] \
    clickhouse-driver

# Install additional database drivers
RUN pip install --no-cache-dir \
    psycopg2-binary \
    pymongo \
    pymssql \
    pyodbc \
    mysqlclient

# Create a custom requirements file for ClickHouse
RUN echo "clickhouse-connect[sqlalchemy]>=0.6.0" > /tmp/clickhouse_requirements.txt && \
    echo "clickhouse-driver>=0.2.6" >> /tmp/clickhouse_requirements.txt

# Install in Superset's Python environment as well
RUN pip install --no-cache-dir -r /tmp/clickhouse_requirements.txt

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

# Configure Superset paths
ENV SUPERSET_CONFIG_PATH=/app/superset_config.py
ENV SECRET_KEY=$SECRET_KEY
ENV SUPERSET_HOME=/app/superset_home

# Set Python path to ensure ClickHouse modules are available
ENV PYTHONPATH=/app:/usr/local/lib/python3.11/site-packages:$PYTHONPATH

# Volume mount point for persistent data
# This will be mounted by Railway configuration
VOLUME ["/app/superset_home"]

# Switch to superset user for security
USER superset

# Expose port (Railway will map this automatically)
EXPOSE 8088

ENTRYPOINT ["./superset_init.sh"]
