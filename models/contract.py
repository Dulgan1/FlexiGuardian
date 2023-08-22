#!/usr/bin/python3
""" Contract Class defined """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Contract(BaseModel, Base):
    __tablename__ = "contracts"
    def __init__(self):
        pass

