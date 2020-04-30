#!/usr/bin/python3
""" API """
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from models.user import User
import json


@app_views.route('/users',  methods=['GET', 'POST'],
                 strict_slashes=False)
def user():
    """Return list of users"""
    users = []
    if request.method == 'GET':
        all_users = storage.all('User')
        for user in all_users.values():
            users.append(user.to_dict())
        return jsonify(users)
    elif request.method == 'POST':
        if not request.get_json():
            return jsonify('Not a JSON'), 400
        data = request.get_json()
        if not('email' in data):
            return jsonify('Missing email'), 400
        if not('password' in data):
            return jsonify('Missing password'), 400
        new_user = User(**data)
        storage.new(new_user)
        storage.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def user_id(user_id):
    """User id"""
    user = storage.get('User', user_id)
    if not user:
        abort(404)
    if request.method == 'GET':
        return jsonify(user.to_dict())
    elif request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        if not request.get_json():
            return jsonify('Not a JSON'), 400
        data = request.get_json()
        for k, v in data.items():
            setattr(user, k, v)
        storage.save()
        return jsonify(user.to_dict()), 200
