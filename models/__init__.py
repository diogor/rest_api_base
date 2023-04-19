from sqlmodel import SQLModel, create_engine, Session
from config.settings import DATABASE_URL
from .auth import User

__all__ = ["User"]

engine = create_engine(DATABASE_URL)
SQLModel.metadata.create_all(engine)


def commit(object: SQLModel):
    with Session(engine) as session:
        session.add(object)
        session.commit()
        session.refresh(object)
