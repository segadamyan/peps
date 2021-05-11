from .database import Database
from sqlalchemy import Column, INTEGER, String


class Author(Database.BASE):
    __tablename__ = "Author"
    id = Column(INTEGER, primary_key=True)
    name = Column(String, nullable=False)
