from sqlmodel import SQLModel, create_engine, Session
from config.settings import get_settings
from .auth import User

__all__ = ["User"]

engine = create_engine(get_settings().database_url)


def commit(object: SQLModel):
    with Session(engine) as session:
        session.add(object)
        session.commit()
        session.refresh(object)
