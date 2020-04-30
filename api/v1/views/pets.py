#!/usr/bin/python3
"""Contains pets view"""
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, abort, make_response, request
from models import storage, pet, owner

@app_views.route('/pets', 
                 methods=['GET'],
                 strict_slashes=False)
def pets():
    """pets"""
    pets = []
    my_pets = storage.all('Pet').values()
    for my_pet in my_pets:
        pets.append(my_pet.to_dict())
    return jsonify(pets)


@app_views.route('/owners/<string:owner_id>/pets',
                 methods=['GET'],
                 strict_slashes=False)
def pets_owner_id(owner_id):
    """Retrieves a Owner object"""
    pets = []
    my_owner = storage.get('Owner', owner_id)
    if my_owner is None:
        abort(404)
    for my_pet in my_owner.pets:
        pets.append(my_pet.to_dict())
    return jsonify(pets)


@app_views.route('/pets/<string:pet_id>',
                 methods=['GET'],
                 strict_slashes=False)
def pet_id(pet_id):
    """Retrieves a Pet object by id"""
    my_pet = storage.get('Pet', pet_id)
    if my_pet is None:
        abort(404)
    return jsonify(my_pet.to_dict())


@app_views.route('/pets/<string:pet_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def pet_id_delete(pet_id):
    """Deletes a Pet object by id"""
    my_pet = storage.get('Pet', pet_id)
    if my_pet is None:
        abort(404)
    my_pet.delete()
    storage.save()
    return jsonify({})


@app_views.route('owners/<owner_id>/pets',
                 methods=['POST'],
                 strict_slashes=False)
def create_pet(owner_id):
    """Creates a Pet object"""
    my_owner = storage.get('Owner', owner_id)
    if my_owner is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    if 'name' not in request.json:
        abort(400, 'Missing name')
    my_pet = pet.Pet(name=request.json.get('name', ""), owner_id=owner_id)
    storage.new(my_pet)
    my_pet.save()
    return make_response(jsonify(my_pet.to_dict()), 201)


@app_views.route('/pets/<string:pet_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_pet(pet_id):
    """Updates a Pet object"""
    my_pet = storage.get('Pet', pet_id)
    if my_pet is None:
        abort(404)
    if not request.json:
        # return make_response(jsonify({'error': 'Not a JSON'}), 400)
        abort(400, 'Not a JSON')
    for req in request.json:
        if req not in ['id', 'created_at', 'updated_at']:
            setattr(my_pet, req, request.json[req])
    my_pet.save()
    return jsonify(my_pet.to_dict())


if __name__ == "__main__":
    pass
