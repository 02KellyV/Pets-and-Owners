#!/usr/bin/python
""" holds class City"""
import models
from models.base_model import BaseModel, Base

class Pet(BaseModel, Base):
    """Representation of city """
    name = ""
    age = ""
    color = ""
    owner = ""

    def __init__(self, *args, **kwargs):
        """initializes pet"""
        super().__init__(*args, **kwargs)
