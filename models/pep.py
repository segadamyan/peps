from sqlalchemy import Column, INTEGER, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Database
from .pepauthor import PEPAuthor


class PEP(Database.BASE):
    __tablename__ = 'PEP'
    id = Column(INTEGER, primary_key=True)
    pep = Column(INTEGER, nullable=False)
    status_id = Column(INTEGER, ForeignKey("Status.id"), nullable=False)
    title = Column(String, nullable=False)
    type = Column(String, nullable=False)
    created = Column(String, nullable=False)
    authors = relationship("Author", secondary=PEPAuthor, backref="peps")
