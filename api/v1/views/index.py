#!/usr/bin/python3
""" API """
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status',  methods=['GET'], strict_slashes=False)
def status():
    """Status method that returns a JSON: """
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """Stats methods that return the number of objects"""
    objs = ['Amenity', 'City', 'Place', 'Review', 'State', 'User']
    name_objs = ['amenities', 'cities', 'places', 'reviews', 'states', 'users']
    dic_objs = {}
    num_obj = 0
    for clss in objs:
        dic_objs[name_objs[num_obj]] = storage.count(clss)
        num_obj += 1
    return jsonify(dic_objs)
