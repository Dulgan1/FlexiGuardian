#!/usr/bin/python3
""" Module defines both user and review class"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """ User Class Defined """
    __tablename__ = 'users'
    user_name = Column(String(15), nullable=False)
    email = Column(String(128), nullable=False)
    phone = Column(String(15), nullable=False)
    business = relationship('Business', nullable=True)
    image_url = Column(String(500))
    password = Column(String(128), nullable=False)
    rating = Column(Float, default=0.0)

    def __init__(self, *args, **kwargs):
        """Initializes user class instance"""
        super().__init__(*args, **kwargs)


class Review(BaseModel, Base):
    """ Review Class Defined """
    __tablename__ = 'reviews'
    by_user_id = Column(String(60), nullable=False)
    for_user_id = Column(String(60), nullable=False)
    review_body = Column(String(5000), nullable=False)
    rating = Column(Integer, default=0, nullable=False)

    def __init__(self, *args, **kwargs):
        """Initializes Review class instance"""
        super.__init__(*args, **kwargs)
