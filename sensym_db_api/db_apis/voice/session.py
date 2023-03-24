from contextlib import contextmanager
import logging
from typing import Generator

from fastapi import HTTPException, status
from sensym_models.voice_analysis_db import session


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FastAPI app Logging")


def get_db() -> Generator:
    """Get a database session

    Yields:
        Generator:  A database session
    """
    db = session.LocalSession()
    try:
        yield db
        db.commit()
    finally:
        db.close()


@contextmanager
def session_transcation(session):
    try:
        yield session
        session.commit()
    except Exception as error:
        logger.error(error)
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Server Error {error}")
    finally:
        session.close()
        
