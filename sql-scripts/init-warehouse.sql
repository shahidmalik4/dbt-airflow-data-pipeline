-- Create schemas if they don't exist
CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS marts;
CREATE SCHEMA IF NOT EXISTS analytics;

-- Optional: set default privileges for the admin user
GRANT ALL ON SCHEMA raw TO admin;
GRANT ALL ON SCHEMA staging TO admin;
GRANT ALL ON SCHEMA marts TO admin;
GRANT ALL ON SCHEMA analytics TO admin;
