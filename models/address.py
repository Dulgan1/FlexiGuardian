""" Defines the Address model
    Inherits from BaseModel and Base (For relational mapping)
    attr:
        __tablename__ => name of table in SQL database
        state => holds state.
        zipcode => holds zip code.
        addr_line => holds address line.
        business_id => business id for which address object belongs to.
    All attributes are columns in SQL table
    (Object Relational Mapping) """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

class Address(BaseModel, Base):
    __tablename__ = "addresses"
    state = Column(String(30), nullable=False) # state or region
    zipcode = Column(String(30), nullable=False)
    addr_line = Column(String(128), nullable=False)
    business_id = Column(String(60), ForeignKey('businesses.id'),
                         nullable=False)

    def __init__(self, *args, **kwargs):
        """Initializes address instance"""
        super().__init__(*args, **kwargs)
