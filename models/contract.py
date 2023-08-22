#!/usr/bin/python3
""" Contract Class defined """
import models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Contract(BaseModel, Base):

