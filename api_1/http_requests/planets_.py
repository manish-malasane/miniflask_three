from pydantic import parse_obj_as
from typing import List
import pydantic.error_wrappers
from models.datamodels.planets import Planets, PatchPlanet
from dal.dml import insert_resource, upsert_planets, fetch_resource, __delete_resource
from response_validation.response import ResponseValidation
from flask import Blueprint, Response, request, abort
import json
import logging


planets_app = Blueprint("planets", __name__, url_prefix="/api")


@planets_app.route("/planets", methods=["GET"])
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


@planets_app.route("/planet", methods=["POST"])
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
    ResponseValidation(**response_obj)

    return Response(json.dumps(response_obj), status=201, mimetype="application/json")


@planets_app.route("/planet", methods=["DELETE"])
def delete_planet_data():
    planet_id = request.args.get("planet_id")
    result = __delete_resource("planet", "planet_id", planet_id)

    if result == 0:
        return abort(400)

    response_obj = {
        "Message": f"[ INFO ] Record against film id {planet_id} deleted successfully"
    }
    return Response(json.dumps(response_obj), status=200, mimetype="application/json")


@planets_app.route("/planet", methods=["PUT"])
def put_planet_data():
    planet_ = request.json
    try:
        planet_data = Planets(**planet_)
    except pydantic.error_wrappers.ValidationError as ex:
        logging.error(f"{abort(400)} - {ex}")

    url = planet_data.url

    result = upsert_planets(planet_data, url)

    if result:
        msg = "New Record Created Successfully"
    else:
        msg = "Existing record updated successfully"

    response_data = {"Record_Count": result, "Name": planet_data.name, "Message": msg}
    ResponseValidation(**response_data)

    return Response(json.dumps(response_data), status=200, mimetype="application/json")


@planets_app.route("/planet", methods=["PATCH"])
def patch_planet_data():
    planet_ = request.json

    try:
        planet_data = PatchPlanet(**planet_)
    except pydantic.error_wrappers.ValidationError as ex:
        return abort(400) - ex

    url = planet_data.url
    result = upsert_planets(planet_data, url)

    if result:
        msg = "New Record Created Successfully"
    else:
        msg = "Existing Record Updated Successfully"

    response_obj = {
        "Record_Count": result,
        "Name": planet_data.name,
        "Message": msg
    }

    ResponseValidation(**response_obj)

    return Response(
        json.dumps(response_obj),
        status=200,
        mimetype="application/json"
    )
