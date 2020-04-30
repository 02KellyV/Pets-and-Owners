#!/usr/bin/python3
""" holds class State"""
import models
from models.base_model import BaseModel, Base
from models.pet import Pet
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Owner(BaseModel, Base):
    """Representation of state """
    firstname = ""
    lastname = ""

    def __init__(self, *args, **kwargs):
        """initializes state"""
        super().__init__(*args, **kwargs)

    @property
    def pets(self):
        """getter for list of Pet instances related to the state"""
        pet_list = []
        all_pets = models.storage.all(Pet)
        for pet in all_pets.values():
            if pet.owner == self.id:
                pet_list.append(pet)
        return pet_list
