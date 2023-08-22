from models.base_model import BaseModel, Base

class Address(BaseModel, Base):
    __tablename__ = "addresses"
    def __init__(self):
        pass
