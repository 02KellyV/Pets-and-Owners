#!/usr/bin/python3
""" API """
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
import json


@app_views.route('/states',  methods=['GET'], strict_slashes=False)
def states():
    """ All states """
    list_states = []
    all_states = storage.all('State')
    for value in all_states.values():
        list_states.append(value.to_dict())
    return jsonify(list_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state_id(state_id):
    """ state id """
    all_states = storage.all('State')
    for value in all_states.values():
        value = value.to_dict()
        if value['id'] == state_id:
            return jsonify(value)
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def state_id_delete(state_id):
    all_states = storage.all('State')
    for key, value in all_states.items():
        st_id = key.split('.')
        if st_id[1] == state_id:
            storage.delete(value)
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def state_id_post():
    if not request.get_json():
        return jsonify('Not a JSON'), 400
    data = request.get_json()
    if not ('name' in data):
        return jsonify('Missing name'), 400
    new_state = State()
    new_state.name = data['name']
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('states/<state_id>', methods=['PUT'], strict_slashes=False)
def state_id_put(state_id):
    if not request.get_json():
        return jsonify('Not a JSON'), 400

    data = request.get_json()
    all_states = storage.all('State')
    for key, value in all_states.items():
        st_id = key.split('.')
        if st_id[1] == state_id:
            setattr(value, 'name', data['name'])
            storage.save()
            return jsonify(value.to_dict()), 200
    abort(404)
