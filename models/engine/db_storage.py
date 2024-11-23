#!/usr/bin/python3
"""DBStorage engine for sqlalchemy"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import os

classes = {'State': State, 'City': City,
           'User': User, 'Place': Place,
           'Review': Review, 'Amenity': Amenity}


class DBStorage:
    """Class for DBStorage module
    """
    __engine = None
    __session = None

    def __init__(self):
        """instantiates the class attributes"""
        mysql_usr = os.getenv("HBNB_MYSQL_USER")
        mysql_pwd = os.getenv("HBNB_MYSQL_PWD")
        mysql_host = os.getenv("HBNB_MYSQL_HOST", "localhost")
        mysql_db = os.getenv("HBNB_MYSQL_DB")
        self.__engine = create_engine(
            f"mysql+mysqldb://{mysql_usr}:{mysql_pwd}@{mysql_host}/{mysql_db}",
            pool_pre_ping=True)

        if os.getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the current database session (self.__session) all objects
        depending on the class name (argument cls)"""
        all_classes = (State, City, User, Amenity, Place, Review)
        all_objects = {}
        if cls is None:
            for cls_name in all_classes:
                results = self.__session.query(cls_name)
                for row in results:
                    all_objects[f"{State.name}.{row.id}"] = row
        else:
            if type(cls) is str:
                cls = eval(cls)
            query = self.__session.query(cls)
            for elem in query:
                key = "{}.{}".format(type(elem).__name__, elem.id)
                all_objects[key] = elem

        return all_objects

    def new(self, obj=None):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the database; create the current database
        session"""
        Base.metadata.create_all(self.__engine)
        session = sessionmaker(self.__engine, expire_on_commit=False)
        Session = scoped_session(session)
        self.__session = Session()

    def close(self):
        """Public method to close"""
        self.__session.close()
