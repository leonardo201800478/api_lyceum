SET timezone = 'America/Sao_Paulo';

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Usuário da API (FULL ACCESS)
DO
$$
BEGIN
    IF NOT EXISTS (
        SELECT FROM pg_catalog.pg_roles WHERE rolname = 'lyceum_api_user'
    ) THEN
        CREATE USER lyceum_api_user WITH PASSWORD 'Lyceum@DB2024!SecureP@ssw0rd';
    END IF;
END
$$;

GRANT ALL PRIVILEGES ON DATABASE lyceum_production_db TO lyceum_api_user;
GRANT ALL PRIVILEGES ON SCHEMA public TO lyceum_api_user;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL ON TABLES TO lyceum_api_user;

-- Usuário somente leitura
CREATE USER IF NOT EXISTS lyceum_monitor WITH PASSWORD 'Monitor@Lyceum2024!ReadOnly';

GRANT CONNECT ON DATABASE lyceum_production_db TO lyceum_monitor;
GRANT USAGE ON SCHEMA public TO lyceum_monitor;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO lyceum_monitor;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT ON TABLES TO lyceum_monitor;
