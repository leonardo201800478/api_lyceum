from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.declarative import declared_attr
from src.core.database import Base
from datetime import datetime

class BaseModel(Base):
    __abstract__ = True
    
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)