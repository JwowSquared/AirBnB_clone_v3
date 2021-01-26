#!/usr/bin/python3
"""this is a test string"""

from flask import request, abort, jsonify
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<s_id>/cities",
                 strict_slashes=False,
                 methods=["GET", "POST"])
def cities_base(s_id):
    """this is a test string"""
    # GET method
    if request.method == "GET":
        out = []
        state = storage.get(State, s_id)
        if not state:
            abort(404)
        for city in state.cities:
            out.append(city.to_dict())
        return jsonify(out)
    # POST method
    if request.method == "POST":
        if not request.is_json:
            return "Not a JSON", 400
        state = storage.get(State, s_id)
        if not state:
            abort(404)
        kwargs = {"state_id": s_id}
        kwargs.update(request.get_json())
        out = City(**kwargs)
        if "name" not in out.to_dict().keys():
            return "Missing name", 400
        out.save()
        return out.to_dict(), 201


@app_views.route("/cities/<c_id>",
                 strict_slashes=False,
                 methods=["GET", "DELETE", "PUT"])
def cities_id(c_id):
    """this is a test string"""
    # GET method
    if request.method == "GET":
        city = storage.get(City, c_id)
        if not city:
            abort(404)
        return city.to_dict()
    # DELETE method
    if request.method == "DELETE":
        city = storage.get(City, c_id)
        if not city:
            abort(404)
        city.delete()
        storage.save()
        return {}, 200
    # PUT method
    if request.method == "PUT":
        city = storage.get(City, c_id)
        if not city:
            abort(404)
        if not request.is_json:
            return "Not a JSON", 400
        for k, v in request.get_json().items():
            if k not in ["id", "state_id", "created_at", "updated_at"]:
                setattr(city, k, v)
        storage.save()
        return city.to_dict(), 200
