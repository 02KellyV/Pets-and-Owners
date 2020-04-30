#!/usr/bin/python3
""" API """
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.review import Review
import json


@app_views.route('places/<place_id>/reviews',  methods=['GET', 'POST'],
                 strict_slashes=False)
def reviews(place_id):
    """ Return of all Reviews"""
    place = storage.get('Place', place_id)
    reviews = []
    if not place:
        abort(404)
    if request.method == 'GET':
        all_reviews = storage.all('Review')
        for review in all_reviews.values():
            review = review.to_dict()
            if review['place_id'] == place_id:
                reviews.append(review)
        return jsonify(reviews)
    if request.method == 'POST':
        if not request.get_json():
            return jsonify('Not a JSON'), 400
        data = request.get_json()
        if not('user_id' in data):
            return jsonify('Missing user_id'), 400
        user = storage.get('User', data['user_id'])
        if not user:
            abort(404)
        if not('text' in data):
            return jsonify('Missing text'), 400
        data['place_id'] = place_id
        new_review = Review(**data)
        storage.new(new_review)
        storage.save()
        return jsonify(new_review.to_dict()), 201


@app_views.route('reviews/<review_id>',  methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def review_id(review_id):
    """Return a review"""
    review = storage.get('Review', review_id)
    if not review:
        abort(404)
    if request.method == 'GET':
        return jsonify(review.to_dict())
    elif request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        if not request.get_json():
            return jsonify('Not a JSON'), 400
        data = request.get_json()
        for k, v in data.items():
            setattr(review, k, v)
        storage.save()
        return jsonify(review.to_dict()), 200
