#!/usr/bin/python3
import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
"""This is the db_storage module"""


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
