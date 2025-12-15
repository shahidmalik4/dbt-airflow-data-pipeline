#!/bin/bash
set -e

# Load environment variables
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

# Function to build and start selected services
start_services() {
  local services=("$@")
  if [ "${#services[@]}" -eq 0 ]; then
    echo "=== Building ALL services ==="
    docker compose build
    echo "=== Starting ALL services ==="
    docker compose up -d
  else
    echo "=== Building selected services ==="
    docker compose build "${services[@]}"
    echo "=== Starting selected services ==="
    docker compose up -d "${services[@]}"
  fi
  echo "=== Services started ==="
}

# Menu
echo "Select an option:"
echo "1) Start ALL services"
echo "2) Start Airflow (webserver + scheduler) + postgres_analytics"
echo "3) Start FastAPI + postgres_analytics"
echo "4) Start Metabase + postgres_analytics"
echo "5) Rebuild project (all Docker images)"
echo "6) Exit"

read -rp "Enter your choice [1-6]: " choice

case $choice in
  1)
    echo "Starting ALL services..."
    start_services
    ;;
  2)
    echo "Starting Airflow (webserver + scheduler) + postgres_analytics..."
    start_services airflow-webserver airflow-scheduler postgres_analytics
    ;;
  3)
    echo "Starting FastAPI + postgres_analytics..."
    start_services fastapi postgres_analytics
    ;;
  4)
    echo "Starting Metabase + postgres_analytics..."
    start_services metabase metabase_db postgres_analytics
    ;;
  5)
    echo "Rebuilding all Docker images..."
    docker compose build --no-cache
    echo "Build complete! You can now start services using options 1-4."
    ;;
  6)
    echo "Exiting..."
    exit 0
    ;;
  *)
    echo "Invalid choice. Exiting."
    exit 1
    ;;
esac

echo ""
echo "=== Running Containers ==="
docker compose ps