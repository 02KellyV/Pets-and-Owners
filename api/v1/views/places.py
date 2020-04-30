#!/usr/bin/python3
""" API """
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
import json


@app_views.route('/cities/<city_id>/places',  methods=['GET', 'POST'],
                 strict_slashes=False)
def places_city(city_id):
    """
    places of city
    """
    places = []
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    if request.method == 'POST':
        if not request.get_json():
            return jsonify('Not a JSON'), 400
        data = request.get_json()
        if not('user_id' in data):
            return jsonify('Missing user_id'), 400
        user = storage.get('User', data['user_id'])
        if not user:
            abort(404)
        if not('name' in data):
            return jsonify('Missing name'), 400
        data['city_id'] = city_id
        new_place = Place(**data)
        storage.new(new_place)
        storage.save()
        return jsonify(new_place.to_dict()), 201
    if request.method == 'GET':
        all_places = storage.all('Place')
        for obj in all_places.values():
            obj = obj.to_dict()
            if obj['city_id'] == city_id:
                places.append(obj)
        return jsonify(places)


@app_views.route('/places/<place_id>',  methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def place_id(place_id):
    """
    return a Place
    """
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    if request.method == 'GET':
        return jsonify(place.to_dict())
    elif request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        if not request.get_json():
            return jsonify('Not a JSON'), 400
        data = request.get_json()
        for k, v in data.items():
            if k != 'user_id' and k != 'city_id':
                setattr(place, k, v)
        storage.save()
        return jsonify(place.to_dict()), 200
