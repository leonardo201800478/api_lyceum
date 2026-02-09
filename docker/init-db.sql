-- ==============================================
-- INITIALIZATION SCRIPT FOR LYCEUM DATABASE
-- Executed automatically when PostgreSQL starts
-- ==============================================

-- Set timezone
SET timezone = 'America/Sao_Paulo';

-- Create useful extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create read-only user for monitoring (optional)
CREATE USER lyceum_monitor WITH PASSWORD 'Monitor@Lyceum2024!ReadOnly';
GRANT CONNECT ON DATABASE lyceum_production_db TO lyceum_monitor;
GRANT USAGE ON SCHEMA public TO lyceum_monitor;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO lyceum_monitor;

-- Set default privileges for future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public 
GRANT SELECT ON TABLES TO lyceum_monitor;

-- Log initialization
DO $$
BEGIN
    RAISE NOTICE '✅ Database lyceum_production_db initialized successfully';
    RAISE NOTICE '📅 Timezone: %', current_setting('TIMEZONE');
    RAISE NOTICE '🔐 User: lyceum_api_user created';
    RAISE NOTICE '👁️  Monitor user: lyceum_monitor created (read-only)';
END $$;