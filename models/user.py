#!/usr/bin/python3
""" User Class defined """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class User:
    __tablename__ = 'users'
    user_name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)
    phone = Column(String(128), nullable=False)
    reviews = relationship('Review', backref='user')
    rating = Column(Integer)

    def __init__(self, *args, **kwargs):
        """Initializes user class instance"""
        super().__init__(*args, **kwargs)

