#!/usr/bin/python3
""" State Module for HBNB project """
import os
from models.base_model import BaseModel
from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship(
            'City', cascade='all, delete-orphan', backref='state')
    else:
        @property
        def cities(self):
            from models import storage
            cities_list = []
            for city in storage.all("City").values():
                if city.state_id == self.id:
                    cities_list.append(city)
            return cities_list
