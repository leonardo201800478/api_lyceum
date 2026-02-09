"""
Modulo core com funcionalidades principais
"""
from .config import settings
from .database import (
    # Engines
    async_engine,
    sync_engine,
    engine,
    
    # Session factories
    AsyncSessionLocal,
    SyncSessionLocal,
    
    # Dependencies
    get_async_session,
    get_sync_session,
    get_db,
    get_sync_db,
    
    # Base para modelos
    Base,
    
    # Funcoes uteis
    check_database_connection,
    init_database,
    close_database_connections,
)

__all__ = [
    'settings',
    'async_engine',
    'sync_engine',
    'engine',
    'AsyncSessionLocal',
    'SyncSessionLocal',
    'get_async_session',
    'get_sync_session',
    'get_db',
    'get_sync_db',
    'Base',
    'check_database_connection',
    'init_database',
    'close_database_connections',
]