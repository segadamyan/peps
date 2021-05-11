from sqlalchemy import Column, INTEGER, ForeignKey, Table
from .database import Database

PEPAuthor = Table(
    'PEPAuthor',
    Database.BASE.metadata,
    Column('author_id', INTEGER, ForeignKey('Author.id')),
    Column('pep_id', INTEGER, ForeignKey('PEP.id'))
)
