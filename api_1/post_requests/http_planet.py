import pydantic.error_wrappers
from models.datamodels.planets import Planets
from flask import Blueprint, Response, request
from resources.people import fetch_resource
from pydantic import parse_obj_as
from typing import List
from dal.dml import insert_resource
import json
from response_validation.response import PostResponse

planet_api = Blueprint("planets", __name__, url_prefix="/api/planets")


@planet_api.route("/get_planets", methods=["GET"])
def get_planets():
    data = fetch_resource("planets")
    planets = data.get("results")
    planets_ = parse_obj_as(List[Planets], planets)
    planets_data = []
    for planet in planets_:
        planet = Planets(**dict(planet))
        data = planet.json()
        planets_data.append(data)
    return Response(json.dumps(planets_data), status=200, mimetype="application/json")


@planet_api.route("/post_planet", methods=["POST"])
def post_planets_data():
    planet_ = request.json

    # REQUEST BODY VALIDATION
    try:
        planet_data = Planets(**planet_)
    except pydantic.error_wrappers.ValidationError as ex:
        response_obj = {"message": f"{ex}"}
        return Response(
            json.dumps(response_obj), status=422, mimetype="application/json"
        )

    # BUSINESS LOGIC
    planet_columns = [
        "name",
        "rotation_period",
        "orbital_period",
        "diameter",
        "climate",
        "gravity",
        "terrain",
        "surface_water",
        "population",
        "created",
        "edited",
        "url",
    ]
    planet_values = [
        planet_data.name,
        planet_data.rotation_period,
        planet_data.orbital_period,
        planet_data.diameter,
        planet_data.climate,
        planet_data.gravity,
        planet_data.terrain,
        planet_data.surface_water,
        planet_data.population,
        planet_data.created.strftime("%y-%m-%d"),
        planet_data.edited.strftime("%y-%m-%d"),
        planet_data.url,
    ]

    planet_id = int(planet_data.url.split("/")[-2])
    result = insert_resource(
        "planet", "planet_id", planet_id, planet_columns, planet_values
    )

    if result:
        msg = "Record Created Successfully"
    else:
        response_obj = {"message": "Record already inserted"}

        return Response(
            json.dumps(response_obj), status=409, mimetype="application/json"
        )

    response_obj = {
        "Record_Count": result,
        "Name": planet_data.name,
        "Message": msg,
    }

    # RESPONSE VALIDATION
    PostResponse(**response_obj)

    return Response(json.dumps(response_obj), status=201, mimetype="application/json")
