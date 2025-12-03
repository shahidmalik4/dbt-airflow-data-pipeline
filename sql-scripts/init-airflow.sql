CREATE USER airflow_user WITH PASSWORD 'airflow_password';
CREATE DATABASE airflow_db;
GRANT ALL PRIVILEGES ON DATABASE airflow_db TO airflow_user;
