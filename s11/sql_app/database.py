from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"


class Base(DeclarativeBase): ...


engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autoflush=False, bind=engine)
