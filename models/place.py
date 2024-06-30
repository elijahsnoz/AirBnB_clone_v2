#!/usr/bin/python3
""" Place Module for HBNB project """
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base

# Table for many-to-many relationship between Place and Amenity
place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60), ForeignKey('places.id'), primary_key=True, nullable=False),
                      Column('amenity_id', String(60), ForeignKey('amenities.id'), primary_key=True, nullable=False))

class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'

    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    user = relationship("User", back_populates="places")
    city = relationship("City", back_populates="places")
    reviews = relationship("Review", back_populates="place", cascade="all, delete, delete-orphan")
    amenities = relationship("Amenity", secondary=place_amenity, viewonly=False, back_populates="place_amenities")

    @property
    def amenities(self):
        """Getter attribute that returns the list of Amenity instances based on the attribute amenity_ids"""
        from models import storage
        all_amenities = storage.all(Amenity)
        place_amenities = [amenity for amenity in all_amenities.values() if amenity.id in self.amenity_ids]
        return place_amenities

    @amenities.setter
    def amenities(self, amenity_obj):
        """Setter attribute that handles append method for adding an Amenity.id to the attribute amenity_ids"""
        if isinstance(amenity_obj, Amenity):
            self.amenity_ids.append(amenity_obj.id)
