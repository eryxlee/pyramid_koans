from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    Float,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()



class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(Unicode(64), unique=True, nullable=False)
    author = Column(Unicode(32), nullable=True)
    desc = Column(Unicode, nullable=True)
    ISBN = Column(Unicode(20), nullable=True)
    price = Column(Float, nullable=True)

    def __init__(self, name, author, desc, ISBN, price):
        self.name = name
        self.author = author
        self.desc = desc
        self.ISBN = ISBN
        self.price = price

