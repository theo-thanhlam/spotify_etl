from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os
from dotenv import load_dotenv
from .. import logger  # Adjust import based on your project structure

# Load environment variables
load_dotenv(dotenv_path=".env")

# Global variables for engine and session factory
_engine = None
_SessionFactory = None

def get_engine():
    """Creates or returns the existing SQLAlchemy engine."""
    global _engine
    if _engine is None:
        db_url = os.getenv("DB_URL")
        if not db_url:
            raise ValueError("DB_URL is not set in the environment variables.")
        
        _engine = create_engine(db_url)
        logger.info("Created new database engine")

    return _engine

def get_session() -> Session:
    """Creates and returns a new SQLAlchemy session."""
    global _SessionFactory
    if _SessionFactory is None:
        _SessionFactory = sessionmaker(bind=get_engine())
        logger.info("Initialized session factory")

    return _SessionFactory()  # Returns a new session instance
