#!/usr/bin/python3
import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session
from models.state import State
from models.city import City
"""This is the db_storage module"""

Base = declarative_base()


class DBStorage:
    """New Engine"""
    __engine = None
    __session = None

    def __init__(self):
        """create the engine"""
        self.__engine = create_engine(
            'mysql+mysql://{}:{}@localost/{}'.format(
                'HBNB_MYSQL_USER', 'HBNB_MYSQL_PWD',
                'HBNB_MYSQL_DB'), pool_pre_ping=True)

        """drop all tables if the environment variable HBNB_ENV is
        equal to test"""
        if os.getenv("HBNB_ENV") == "test":
            metadata = MetaData()
            metadata.bind = self.__engine
            metadata.reflect()
            metadata.drop_all()

    def all(self, cls=None):
        """query on the current database session (self.__session) all objects
        depending of the class name"""
        Session = sessionmaker(bind=self.__engine)
        self.__session = Session()
        if cls is None:
            self.__session.query().all()
        else:
            self.__session.query(cls).all()

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the database (feature of SQLAlchemy)"""
        Base.metadata.create_all(self.__engine)
        session = sessionmaker(self.__engine, expire_on_commit=False)
        Session = scoped_session(session)
        Session()