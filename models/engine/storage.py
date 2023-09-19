#!/usr/bin/python3
"""Defines and specifies connection to Storage engine MySQL"""
import models
from models.address import Address
from models.base_model import Base, BaseModel
from models.business import Business
from models.contract import Contract
from models.user import User, Review
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {'Address': Address, 'Business': Business, 'Contract': Contract,
           'Review': Review, 'User': User}

class Storage:
    """The storage class for saving, reloading and connecting to database"""
    __engine = None
    __session = None

    def __init__(self):
        """Initializes the storage class """
        FG_MYSQL_USER = getenv('FG_MYSQL_USER')
        FG_MYSQL_PWD = getenv('FG_MYSQL_PWD')
        FG_MYSQL_HOST = getenv('FG_MYSQL_HOST')
        FG_MYSQL_DB = getenv('FG_MYSQL_DB')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            FG_MYSQL_USER,
            FG_MYSQL_PWD,
            FG_MYSQL_HOST,
            FG_MYSQL_DB))

    def all(self, cls=None):
        """Gets all objects in data of passed class cls"""
        temp_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    temp_dict[key] = obj
        return (temp_dict)

    def session(self):
        return self.__session

    def reload(self):
        """Loads data from database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def new(self, obj):
        """Adds newly creates object to database"""
        self.__session.add(obj)

    def save(self):
        """Saves changes to database"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes a data of object obj"""
        if obj is not None:
            self.__session.delete(obj)
            return "Success"
        else:
            return "Failed, Null object"

    def get(self, cls, id):
        """Gets data linked to id and of class cls"""
        if cls not in classes.values():
            return None

        all_cls = models.storage.all(cls)
        for value in all_cls.values():
            if (value.id == id):
                return value
    def get_user(self,  data):
        """Gets object id by data of object, applies only User class for now"""
        user = self.__session.query(User).filter(User.email==data).first()
        if user:
            return user
        else:
            return None

    def close(self):
        """Closes db connection"""
        self.__session.remove()
