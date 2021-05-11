from sqlalchemy import Column, INTEGER, String
from .database import Database


class Status(Database.BASE):
    __tablename__ = "Status"
    id = Column(INTEGER, primary_key=True)
    value = Column(String, nullable=False)
