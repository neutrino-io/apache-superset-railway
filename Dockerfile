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
# First install clickhouse-driver and its dependencies
RUN pip install --no-cache-dir \
    clickhouse-driver \
    clickhouse-sqlalchemy

# Install additional database drivers
RUN pip install --no-cache-dir \
    psycopg2-binary \
    pymongo \
    pymssql \
    pyodbc \
    mysqlclient

# Create a custom requirements file for ClickHouse
RUN echo "clickhouse-driver>=0.2.6" > /tmp/clickhouse_requirements.txt && \
    echo "clickhouse-sqlalchemy>=0.2.0" >> /tmp/clickhouse_requirements.txt

# Install in Superset's Python environment as well
RUN pip install --no-cache-dir -r /tmp/clickhouse_requirements.txt

ENV ADMIN_USERNAME $ADMIN_USERNAME
ENV ADMIN_EMAIL $ADMIN_EMAIL
ENV ADMIN_PASSWORD $ADMIN_PASSWORD

COPY /config/superset_init.sh ./superset_init.sh
RUN chmod +x ./superset_init.sh

COPY /config/superset_config.py /app/
ENV SUPERSET_CONFIG_PATH /app/superset_config.py
ENV SECRET_KEY $SECRET_KEY

# Set Python path to ensure ClickHouse modules are available
ENV PYTHONPATH /app:/usr/local/lib/python3.11/site-packages:$PYTHONPATH

USER superset

ENTRYPOINT [ "./superset_init.sh" ]