import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool

# Get DATABASE_URL from environment
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:password@db:5432/seoanalyzer"
)

# Create engine with proper settings for production
engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool,  # Avoid connection pool issues in Docker
    echo=False,
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base for all models
Base = declarative_base()

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Create all tables on startup"""
    Base.metadata.create_all(bind=engine)
