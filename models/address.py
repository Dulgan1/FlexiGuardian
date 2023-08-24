from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy import relationship

class Address(BaseModel, Base):
    __tablename__ = "addresses"
    country = Column(String(30), nullable=False)
    state = Column(String(30), nullable=False) # state or region
    zipcode = Column(String(30), nullable=False)
    addr_line = Column(String(128), nullable=False)
    business_id = Column(String(60), ForeignKey('businesses.id'),
                         nullable=False)

    def __init__(self, *args, **kwargs):
        """Initializes address instance"""
        super().__init__(*args, **kwargs)
