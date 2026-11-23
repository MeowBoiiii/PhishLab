from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Engine SQLAlchemy do komunikacji z bazą PostgreSQL
engine = create_engine(
    settings.sync_database_url,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Generator sesji bazy danych wstrzykiwany jako zależność (Dependency Injection) do endpointów."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

