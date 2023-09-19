#!/usr/bin/python3
""" Defines Base Model for all models of FlexiGuardian project"""
from datetime import datetime
import models
from sqlalchemy import Column, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()


class BaseModel:
    """ BaseModel Class: the class which any other class inherits from :)"""
    id = Column(String(60), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        if kwargs:
            for k, v in kwargs.items():
                if k != '__class__':
                    setattr(self, k, v)
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = self.created_at

    def __str__(self):
        obj_dict = self.to_dict()
        """Returns string representation of BaseModel instance"""
        return "[{}] ({}) {}\n [ObjectDictionary] {}".format(
                self.__class__.__name__,
                self.id, self.__dict__, obj_dict)

    def to_dict(self) -> dict:
        """Returns a dictionary of class instance"""
        temp = self.__dict__.copy()
        temp['created_at'] = datetime.isoformat(temp['created_at'])
        temp['updated_at'] = datetime.isoformat(temp['updated_at'])
        temp['__class__'] = self.__class__.__name__
        if '_sa_instance_state' in temp:
            del temp['_sa_instance_state']
        return temp

    def save(self):
        """Saves instance to storage (Database)"""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()
