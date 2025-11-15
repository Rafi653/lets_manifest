# Postgres Initialization Script

-- This script runs when the PostgreSQL container is first initialized

-- Create extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- For text search

-- Note: The database and user are already created by the POSTGRES_DB and POSTGRES_USER
-- environment variables in docker-compose.yml

-- Grant necessary permissions
GRANT ALL PRIVILEGES ON DATABASE lets_manifest_dev TO lets_manifest_user;

-- Set default search path
ALTER DATABASE lets_manifest_dev SET search_path TO public;
