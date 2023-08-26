from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
class Business(BaseModel, Base):
    __tablename__ = "businesses"
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    address = relationship('Address', backref='business')
    contacts = Column(JSON)
    description = Column(String(5000), nullable=False)
    image_url = Column(String(500), nullable=True)

    def __init__(self, *args, **kwargs):
        super().__init(*args,**kwargs)
