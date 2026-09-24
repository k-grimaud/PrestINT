import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker


class Base(DeclarativeBase):
    pass


engine = create_engine(
    os.environ["DATABASE_URL"]
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
