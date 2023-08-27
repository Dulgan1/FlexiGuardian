#!/usr/bin/python3
""" Contract Class defined """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, JSON
from sqlalchemy.orm import relationship


class Contract(BaseModel, Base):
    __tablename__ = "contracts"
    c_type = Column(Integer, nullable=False)
    seller_id = Column('seller', String(60), nullable=False)
    buyer_id = Column('buyer', String(60), nullable=False)
    pro_ser_name = Column(String(128), nullable=False)
    desc = Column(JSON, nullable=False)
    disputed = Column(Integer, default=0)
    status = Column(String(10), nullable=False)
    amount = Column(Float, nullable=False)

    def __init__(self, *args, **kwargs):
        super.__init__(*args, **kwargs)
