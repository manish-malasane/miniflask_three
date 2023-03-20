from flask import Blueprint, Response, request, abort
from dal.dml import __delete_resource

import json


delete_endpoint = Blueprint("delete_request", __name__, url_prefix="/api")


@delete_endpoint.route("/film", methods=["DELETE"])
def delete_film_data():
    film_id = request.args.get("film_id")
    result = __delete_resource("film", "film_id", film_id)

    if result == 0:
        return abort(400)

    response_obj = {
        "Message": f"[ INFO ] Record against film id {film_id} deleted successfully"
    }
    return Response(json.dumps(response_obj), status=200, mimetype="application/json")


@delete_endpoint.route("/character", methods=["DELETE"])
def delete_char_data():
    char_id = request.args.get("char_id")
    result = __delete_resource("characters", "char_id", char_id)

    if result == 0:
        return abort(400)

    response_obj = {
        "Message": f"[ INFO ] Record against film id {char_id} deleted successfully"
    }
    return Response(json.dumps(response_obj), status=200, mimetype="application/json")


@delete_endpoint.route("/planet", methods=["DELETE"])
def delete_planet_data():
    planet_id = request.args.get("planet_id")
    result = __delete_resource("planet", "planet_id", planet_id)

    if result == 0:
        return abort(400)

    response_obj = {
        "Message": f"[ INFO ] Record against film id {planet_id} deleted successfully"
    }
    return Response(json.dumps(response_obj), status=200, mimetype="application/json")


@delete_endpoint.route("/specie", methods=["DELETE"])
def delete_specie_data():
    specie_id = request.args.get("specie_id")
    result = __delete_resource("species", "species_id", specie_id)

    if result == 0:
        return abort(400)

    response_obj = {
        "Message": f"[ INFO ] Record against specie id {specie_id} deleted successfully"
    }
    return Response(json.dumps(response_obj), status=200, mimetype="application/json")


@delete_endpoint.route("/starship", methods=["DELETE"])
def delete_starship_data():
    starship_id = request.args.get("starship_id")
    result = __delete_resource("starship", "starship_id", starship_id)

    if result == 0:
        return abort(400)

    response_obj = {
        "Message": f"[ INFO ] Record against starship_id {starship_id} deleted successfully"
    }
    return Response(json.dumps(response_obj), status=200, mimetype="application/json")


@delete_endpoint.route("/vehicle", methods=["DELETE"])
def delete_vehicle_data():
    vehicle_id = request.args.get("vehicle_id")
    result = __delete_resource("vehicle", "vehicle_id", vehicle_id)

    if result == 0:
        return abort(400)

    response_obj = {
        "Message": f"[ INFO ] Record against vehicle_id {vehicle_id} deleted successfully"
    }
    return Response(json.dumps(response_obj), status=200, mimetype="application/json")
