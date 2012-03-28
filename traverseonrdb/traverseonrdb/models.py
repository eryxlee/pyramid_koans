from sqlalchemy import (
    Column,
    Integer,
    Text,
    and_,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class MyCat(Base):
    __tablename__ = 'mycat'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    pid = Column(Integer)
    desc = Column(Text)

    def __init__(self, name, pid, desc):
        self.name = name
        self.pid = pid
        self.desc = desc
        
    def __getitem__(self, key):
        session= DBSession()
        
        is_file = False
        try:
            key.index(".")
            is_file = True
        except: pass
        
        if is_file:
            item = session.query(MyFile).filter(and_(MyFile.name==key, MyFile.cat==self.id)).first()
        else:
            item = session.query(MyCat).filter(and_(MyCat.name==key, MyCat.pid==self.id)).first()

        if item is None:
            raise KeyError(key)

        item.__parent__ = self
        item.__name__ = key
        return item

    def get(self, key, default=None):
        try:
            item = self.__getitem__(key)
        except KeyError:
            item = default
        return item

    def listall(self):
        session= DBSession()
        cats = session.query(MyCat).filter(MyCat.pid==self.id).all()
        files = session.query(MyFile).filter(MyFile.cat==self.id).all()
        return cats + files

class MyFile(Base):
    __tablename__ = 'myfile'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    cat = Column(Integer)
    save_path = Column(Text)
    desc = Column(Text)

    def __init__(self, name, cat, save_path, desc):
        self.name = name
        self.cat = cat
        self.save_path = save_path
        self.desc = desc


class MyRoot(object):
    __name__ = None
    __parent__ = None

    def __getitem__(self, key):
        session= DBSession()

        item = session.query(MyCat).filter(and_(MyCat.name==key, MyCat.pid==0)).first()
        if item is None:
            raise KeyError(key)

        item.__parent__ = self
        item.__name__ = key
        return item

    def get(self, key, default=None):
        try:
            item = self.__getitem__(key)
        except KeyError:
            item = default
        return item

    def __iter__(self):
        session= DBSession()
        query = session.query(MyCat).filter(MyCat.pid==0)
        return iter(query)

root = MyRoot()

def root_factory(request):
    return root

