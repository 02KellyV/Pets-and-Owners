#!/usr/bin/python3
""" API """
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
import json


@app_views.route('/amenities',  methods=['GET', 'POST'],
                 strict_slashes=False)
def amenities():
    """
    view for Amenity objects
    """
    aminities = []
    if request.method == 'GET':
        all_amenities = storage.all('Amenity')
        for obj in all_amenities.values():
            aminities.append(obj.to_dict())
        return jsonify(aminities)
    elif request.method == 'POST':
        if not request.get_json():
            return jsonify('Not a JSON'), 400
        data = request.get_json()
        if not('name' in data):
            return jsonify('Missing name'), 400
        new_amenity = Amenity()
        new_amenity.name = data['name']
        storage.new(new_amenity)
        storage.save()
        return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',  methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def amenity_id(amenity_id):
    """
    Amenity
    """
    amenity = storage.get('Amenity', amenity_id)
    if not amenity:
        abort(404)
    if request.method == 'GET':
        return jsonify(amenity.to_dict())
    elif request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        if not request.get_json():
            return jsonify('Not a JSON'), 400
        data = request.get_json()
        setattr(amenity, 'name', data['name'])
        storage.save()
        return jsonify(amenity.to_dict()), 200
