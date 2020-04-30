#!/usr/bin/python3
""" API """
from flask import Flask, jsonify, abort, request
from models import storage
from models.pet import Pet
from models.owner import Owner
from api.v1.views import app_views
import json


@app_views.route('/owners', methods=['GET', 'POST'],
                 strict_slashes=False)
def owners():
    """
    All owners
    """
    owners = []
    if request.method == 'GET':
        all_dict_owners = []
        all_owners = storage.all('Owner').values()
        for obj in all_owners:
            all_dict_owners.append(obj.to_dict())
        return jsonify(all_dict_owners)
    elif request.method == 'POST':
        if not request.get_json():
            return jsonify('Not a Json'), 400
        data = request.get_json()
        if not('firstname' in data):
            return jsonify('Not firstname'), 400
        new_owner = Owner(**data)
        storage.new(new_owner)
        storage.save()
        return jsonify(new_owner.to_dict()), 201


@app_views.route('/owners/<owner_id>', methods=['PUT', 'DELETE'],
                 strict_slashes=False)
def owner_id(owner_id):
    """
    Owner
    """
    owner = storage.get('Owner', owner_id)
    if not owner:
        abort(404)
    if request.method == 'PUT':
        if not request.get_json:
            return jsonify('Not a Json'), 400
        data = request.get_json()
        for k, v in data.items():
            setattr(owner, k, v)
        owner.save()
        return jsonify(owner.to_dict()), 201
    elif request.method == 'DELETE':
        storage.delete(owner)
        storage.save()
        return ({}), 200


@app_views.route('/owners/<owner_id>/pets',  methods=['GET'],
                 strict_slashes=False)
def owner_pet(owner_id):
    """
    All pets for a owner
    """
    list_pet = []
    owner = storage.get('Owner', owner_id)
    if not owner:
        abort(404)
    pets = storage.all('Pet')
    if obj in pets.values():
        obj = obj.to_dict()
        if obj['owner'] == owner_id:
            list_pet.append(obj)
    return jsonify(list_pet)
