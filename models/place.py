#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from models.review import Review
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
import os

place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60), ForeignKey(
                          'places.id'), primary_key=True, nullable=False),
                      Column('amenity_id', String(60), ForeignKey(
                          'amenities.id'), primary_key=True, nullable=False)
                      )


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'

    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []

    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship(
            "Review", cascade="all, delete-orphan",
            viewonly=False, backref="place")
        amenities = relationship(
            "Amenity", secondary='place_amenity', viewonly=False)
    else:
        @property
        def reviews(self):
            """getter attribute reviews that returns the list of Review
            instances with place_id equals to the current Place.id"""
            from models import storage
            return [review for review in storage.all(Review).values()
                    if self.id == review.place_id]

        @property
        def amenities(self):
            """Getter attribute amenities that returns the list of Amenity
            instances based on the attribute amenity_ids that contains all
            Amenity.id linked to the Place"""
            from models import storage
            from models.amenity import Amenity
            return [amnty for amnty in storage.all(Amenity)]

        @amenities.setter
        def amenities(self, amenity=None):
            """Setter attribute amenities that handles append method for
            adding an Amenity.id to the attribute amenity_ids"""
            from models.amenity import Amenity
            if isinstance(amenity, Amenity):
                new_amenity = 'Amenity' + '.' + amenity.id
                self.amenity_ids.append(new_amenity)
