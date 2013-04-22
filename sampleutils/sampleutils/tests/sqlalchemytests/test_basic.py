__author__ = 'eryxlee'

import unittest
import datetime

from sqlalchemytests import create_engine, ForeignKey
from sqlalchemytests import Column, Date, Integer, String
from sqlalchemytests.ext.declarative import declarative_base
from sqlalchemytests.orm import relationship, backref, sessionmaker

Base = declarative_base()

class Artist(Base):
    """"""
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    #----------------------------------------------------------------------
    def __init__(self, name):
        """"""
        self.name = name


class Album(Base):
    """"""
    __tablename__ = "albums"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(Date)
    publisher = Column(String)
    media_type = Column(String)

    artist_id = Column(Integer, ForeignKey("artists.id"))
    artist = relationship("Artist", backref=backref("albums", order_by=id))

    #----------------------------------------------------------------------
    def __init__(self, title, release_date, publisher, media_type):
        """"""
        self.title = title
        self.release_date = release_date
        self.publisher = publisher
        self.media_type = media_type


class SQLAlchemyBasicTests(unittest.TestCase):
    def setUp(self):
        engine = create_engine('sqlite://', echo=True)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        pass

    def tearDown(self):
        pass

    def test_table_create(self):
        obj = self.session.query(Artist).first()

        assert obj is None

    def test_table_insert(self):
        # Create an artist
        new_artist = Artist("Newsboys")
        new_artist.albums = [Album("Read All About It",
            datetime.date(1988,12,01),
            "Refuge", "CD")]

        # Add the record to the session object
        self.session.add(new_artist)
        # commit the record the database
        self.session.commit()

        artist, album = self.session.query(Artist, Album).filter(Artist.id==Album.artist_id).filter(Album.title=="Read All About It").first()

        assert artist.name == "Newsboys"
        assert album.publisher == "Refuge"

    def test_table_insertall(self):
        # Add several artists
        self.session.add_all([
            Artist("MXPX"),
            Artist("Kutless"),
            Artist("Thousand Foot Krutch")
        ])
        self.session.commit()

        count = self.session.query(Artist).count()

        assert count == 3