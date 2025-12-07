#!/bin/bash
set -e

# Load environment variables from .env
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

echo "=== Step 1: Build Docker images ==="
docker compose up -d --build

# Wait for Airflow Postgres to be ready
echo "=== Step 2: Waiting for Airflow Postgres to be ready ==="
until docker compose exec postgres_airflow pg_isready -U "$AIRFLOW_USER" > /dev/null 2>&1; do
  echo "Waiting for postgres_airflow..."
  sleep 2
done

# Initialize Airflow DB
echo "=== Step 3: Initialize Airflow metadata database ==="
docker compose run --rm airflow-webserver airflow db init

# Create Admin user for Airflow web UI
echo "=== Step 4: Create Airflow UI admin user ==="
docker compose run --rm airflow-webserver \
    airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin || true

# Start all Airflow containers
echo "=== Step 5: Start Airflow webserver and scheduler ==="
docker compose up -d

echo "Airflow setup complete!"
echo "Web UI: http://localhost:8080"
echo "Username: admin"
echo "Password: admin"
