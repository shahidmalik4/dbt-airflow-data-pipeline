#!/bin/bash
set -e

# Load environment variables from .env
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

echo "=== Step 1: Build Docker images ==="
docker compose up -d --build

# Wait for Airflow Postgres
echo "=== Step 2: Waiting for Airflow Postgres ==="
until docker compose exec postgres_airflow pg_isready -U "$AIRFLOW_USER" > /dev/null 2>&1; do
  echo "Waiting for postgres_airflow..."
  sleep 2
done

# Wait for Analytics Postgres
echo "=== Step 3: Waiting for Analytics Postgres ==="
until docker compose exec postgres_analytics pg_isready -U "$POSTGRES_USER" > /dev/null 2>&1; do
  echo "Waiting for postgres_analytics..."
  sleep 2
done

# Initialize Airflow DB
echo "=== Step 4: Initialize Airflow metadata database ==="
docker compose run --rm airflow-webserver airflow db init

# Create Admin user for Airflow web UI
echo "=== Step 5: Create Airflow UI admin user ==="
docker compose run --rm airflow-webserver \
    airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin || true

# Add Postgres connection to Airflow
echo "=== Step 6: Add Postgres connection to Airflow ==="
docker compose run --rm airflow-webserver airflow connections add postgres_local \
    --conn-uri "postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres_analytics:5432/${POSTGRES_DB}" || true

# Start all containers
echo "=== Step 7: Start all containers ==="
docker compose up -d

echo "=== Setup Complete! ==="
echo ""
echo "Airflow:"
echo "  Web UI: http://localhost:8080"
echo "  Username: admin"
echo "  Password: admin"
echo ""
echo "FastAPI:"
echo "  API URL: http://localhost:8000"
echo ""
echo "Metabase:"
echo "  Web UI: http://localhost:3000"
echo ""
echo "PostgreSQL Databases:"
echo "  Airflow Metadata: postgres_airflow (Port: ${AIRFLOW_PORT})"
echo "  Analytics / Warehouse: postgres_analytics (Port: ${POSTGRES_PORT})"
echo "  Metabase DB: metabase_db (internal)"
echo ""
echo "All services are up and running!"
