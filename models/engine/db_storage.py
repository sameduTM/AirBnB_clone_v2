#!/usr/bin/env python3
"""engine DBStorage"""
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """class DBStorage"""
    __engine = None
    __session = None
    __objects = {}

    def __init__(self):
        """instantiates the engine"""
        mysql_usr = os.getenv('HBNB_MYSQL_USER')
        mysql_pwd = os.getenv('HBNB_MYSQL_PWD')
        mysql_host = os.getenv('HBNB_MYSQL_HOST', 'localhost')
        mysql_db = os.getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine(
            f'mysql+mysqldb://{mysql_usr}:{mysql_pwd}@{mysql_host}/{mysql_db}',
            pool_pre_ping=True)

        if os.getenv("HBNB_ENV") == 'test':
            """drop all tables if the environment variable
            HBNB_ENV is equal to test"""

    def all(self, cls=None):
        """query on the current database session (self.__session) all objects
        depending of the class name"""
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review
        classes = {
            'User': User, 'Place': Place,
            'State': State, 'City': City, 'Amenity': Amenity,
            'Review': Review
        }
        if cls:
            table_name = classes[cls].__tablename__
            txt = f'SELECT * FROM {table_name}'
            results = self.__session.execute(text(txt))
            for result in results:
                DBStorage.__objects[f'{cls}.{result.id}'] = result._mapping
        else:
            for cls_name in classes:
                table_name = classes[cls_name].__tablename__
                txt = f'SELECT * FROM {table_name}'
                results = self.__session.execute(text(txt))
                for result in results:
                    DBStorage.__objects[f'{cls.__name__}.{result.id}'] = result
        return DBStorage.__objects

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the database"""
        from models.base_model import Base
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review
        Base.metadata.create_all(self.__engine)
        session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session)
        self.__session = Session()
