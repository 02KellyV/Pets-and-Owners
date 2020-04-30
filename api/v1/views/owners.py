#!/usr/bin/python3
""" API """
from flask import Flask, jsonify, abort, request
from models import storage
import json


@app_views.route('/owners',  methods=['GET'],
                 strict_slashes=False)
def owners():
    """
    All owners
    """
    owners = []
    all_owners = storage.all('Owner')
    return jsonify(all_owners.to_dict())
