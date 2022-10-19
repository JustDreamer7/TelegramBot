from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.local_settings import DB_URL
from config.structure_db import Base


def create_db():
    engine = create_engine(DB_URL)
    Base.metadata.create_all(engine)


def connect_to_db():
    engine = create_engine(DB_URL)
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)
    db_session = session()
    return db_session