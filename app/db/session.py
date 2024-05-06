"""
Database session script
"""

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from app.config.settings import setting

url: str = f"{setting.SQLALCHEMY_DATABASE_URI}"
engine: Engine = create_engine(url, pool_pre_ping=True, future=True, echo=True)


async def get_session() -> Session:
    """
    Get an asynchronous session to the database
    :return session: Session for database connection
    :rtype session: Session
    """
    with Session(bind=engine, expire_on_commit=False) as session:
        return session
