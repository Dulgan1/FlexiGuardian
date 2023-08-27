#!/usr/bin/python3
from models.base_model import Base, BaseModel

class Admin(BaseModel, Base):
    """Tags a user by user_id as Admin"""
    __tablename__ = "admins"
    user_id = Column(String(60), nullable=False)

    def __init__(self, *args, **kwargs):
        super.__init__(*args, **kwargs)
