from sqlalchemy import Column, INTEGER, String
from .database import Database


class User(Database.BASE):
    __tablename__ = "User"
    id = Column(INTEGER, primary_key=True)
    mail = Column(String, nullable=False)
