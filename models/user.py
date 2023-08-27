#!/usr/bin/python3
""" Module defines both user and review class"""
from models.base_model import BaseModel, Base
from models import storage
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """ User Class Defined """
    __tablename__ = 'users'
    name = Column(String(60), nullable=False)
    user_name = Column(String(15), nullable=False)
    email = Column(String(128), nullable=False)
    phone = Column(String(15), nullable=False)
    business = relationship('Business', backref='user')
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
    rating = Column(Integer, nullable=False)

    def __init__(self, *args, **kwargs):
        """Initializes Review class instance"""
        super.__init__(*args, **kwargs)

def calc_tot_rate(user_id):
    user = storage.get(User, user_id)
    _session = storage.session()
    reviews = _session.query(Review).filter(Review.for_user_id==user_id)
    total = 0
    count = 0
    for review in reviews:
        total += review.rating
        count += 1
    rate_tot = total / count

    user.rating = rate_tot
    storage.save
