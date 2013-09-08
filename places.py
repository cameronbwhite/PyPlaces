#!/usr/bin/env python
# places.database.py
import sqlite3
import IPython
import os
from sqlalchemy import Column, Integer, String, PickleType
from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref, scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
Session = scoped_session(sessionmaker())
engine = None

class Place(Base):
    __tablename__ = 'Places'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    user = Column(String)
    password = Column(String)
    host = Column(String) 
    port = Column(Integer)

    def __init__(self, name, host, port, user, password):
        self.name = name
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def __repr__(self, name):
        return '<Place({})>'.format(name)

class Places(object):
    def __init__(self, database_filename):
        global engine
        engine = create_engine(
            'sqlite:///{}'.format(database_filename))
        Session.configure(
            bind=engine, autoflush=False, 
            expire_on_commit=False)
        path = IPython.utils.path.expand_path(path)
        Base.metadata.create_all(engine)
        Session.commit()

    def add(self, name, host, port, user, password):
        """ Add a place """
        Session.add(Place(name, host, port, user, password))
        Session.commit()

    def get(self, name):
        """ Get the place by its name """
        return Session.query(Place).\
            filter(Place.name == name).\
            one()

    def getAll(self):
        """ Return a list of all the places """
        return Session.query(Place).all()

    def connect(self, name):
        """ Connect to the place by its name """
        place = self.get(name)
        command = 'ssh {}@{} -p {}'.format(
            place.user, place.host ,place.port)
        os.system(command)
