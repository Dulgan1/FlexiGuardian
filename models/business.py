""" Defines the Business model 
    Inherits from BaseModel and Base (For relational mapping)
    attr:
        __tablename__ => name of table in SQL database
        user_id => attribute holds id of user that owns the business
        name => holds name of business
        address => holds address of business
        contacts => for business contact
        description => Business description
        image_url => any image for business
    All attributes are columns in table in SQL table
    (Object Relational Mapping """
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
class Business(BaseModel, Base):
    """Defines class Business"""
    __tablename__ = "businesses"
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    address = relationship('Address', backref='business')
    contacts = Column(String(500))
    description = Column(String(5000), nullable=False)
    image_url = Column(String(500))

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
