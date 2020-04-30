#!/usr/bin/python3
""" API """
from flask import Flask, jsonify, abort, request
from models import storage
import json


@app_views.route('/pets',  methods=['GET'],
                 strict_slashes=False)
def pets():
    """
    All Pets
    """
    pets = []
    all_pets = storage.all('Pets')
    return jsonify(all_pets.to_dict)


@app_views.route('/pets/<pet_id>',  methods=['GET'],
                 strict_slashes=False)
def pet_id(pet_id):
    """
    Pet
    """
    pet = storage.get('Pet', pet_id)
    if not pet:
        abort(404)
    return jsonify(pet.to_dict())
