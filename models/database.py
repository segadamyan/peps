from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine


class Database:
    DB_NAME = "pep.db"
    BASE = declarative_base()
    META = BASE.metadata

    def __init__(self, folder_name: str = None):
        path = f"sqlite:///{folder_name}/{Database.DB_NAME}" if folder_name else f"sqlite:///{Database.DB_NAME}"
        self.engine = create_engine(path, connect_args={'check_same_thread': False}, echo=True)

    def create_db(self):
        Database.META.create_all(self.engine)
