#!/usr/bin/python3
""" API """
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
import json


@app_views.route('/states/<state_id>/cities',  methods=['GET', 'POST'],
                 strict_slashes=False)
def cities(state_id):
    """ All cities """
    state = storage.get('State', state_id)
    cities = []
    if not state:
        abort(404)
    if request.method == 'POST':
        if not request.get_json():
            return jsonify('Not a JSON'), 400
        data = request.get_json()
        if not('name' in data):
            return jsonify('Missing name'), 400
        new_city = City()
        new_city.name = data['name']
        new_city.state_id = state_id
        storage.new(new_city)
        storage.save()
        return jsonify(new_city.to_dict()), 201

    elif request.method == 'GET':
        all_cities = storage.all('City')
        for value in all_cities.values():
            value = value.to_dict()
            if value['state_id'] == state_id:
                cities.append(value)
        return jsonify(cities)


@app_views.route('/cities/<city_id>',  methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def city(city_id):
    """ Return city"""
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    if request.method == 'GET':
        return jsonify(city.to_dict())
    elif request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        if not request.get_json():
            return jsonify('Not a JSON'), 400
        data = request.get_json()
        setattr(city, 'name', data['name'])
        storage.save()
        return jsonify(city.to_dict()), 200
