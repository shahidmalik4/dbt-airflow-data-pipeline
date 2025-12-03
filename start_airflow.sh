#!/bin/bash
set -e

# Step 0: Load environment variables
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

echo "=== Checking for image changes ==="

# Build images if Dockerfile or requirements.txt changed
docker compose build airflow-webserver airflow-scheduler

echo "=== Starting Airflow + Postgres containers ==="
docker compose up -d

echo "Containers started!"
echo "Airflow web UI: http://localhost:8080"
