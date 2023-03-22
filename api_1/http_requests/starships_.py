from pydantic import parse_obj_as
from typing import List
import pydantic.error_wrappers
from models.datamodels.starships import Starships, PatchStarship
from dal.dml import insert_resource, upsert_starships, __delete_resource, fetch_resource
from response_validation.response import ResponseValidation
from flask import Blueprint, Response, request, abort
import json
import logging


starships_app = Blueprint("starships", __name__, url_prefix="/api")


@starships_app.route("/starships", methods=["GET"])
def get_starships():
    data = fetch_resource("starships")
    starships = data.get("results")
    starships_ = parse_obj_as(List[Starships], starships)
    starships_data = []
    for starship in starships_:
        starship = Starships(**dict(starship))
        data = starship.json()
        starships_data.append(data)
    return Response(json.dumps(starships_data), status=200, mimetype="application/json")


@starships_app.route("/starship", methods=["POST"])
def post_starship_data():
    starship_ = request.json
    try:
        starship_data = Starships(**starship_)
    except pydantic.error_wrappers.ValidationError as ex:
        response_obj = {"Message": f"{ex}"}
        return Response(
            json.dumps(response_obj), status=422, mimetype="application/json"
        )

    starship_columns = [
        "name",
        "model",
        "manufacturer",
        "cost_in_credits",
        "length",
        "max_atmosphering_speed",
        "crew",
        "passengers",
        "cargo_capacity",
        "consumables",
        "hyperdrive_rating",
        "MGLT",
        "starship_class",
        "created",
        "edited",
        "url",
    ]

    starship_values = [
        starship_data.name,
        starship_data.model,
        starship_data.manufacturer,
        starship_data.cost_in_credits,
        starship_data.length,
        starship_data.max_atmosphering_speed,
        starship_data.crew,
        starship_data.passengers,
        starship_data.cargo_capacity,
        starship_data.consumables,
        starship_data.hyperdrive_rating,
        starship_data.MGLT,
        starship_data.starship_class,
        starship_data.created.strftime("%y-%m-%d"),
        starship_data.edited.strftime("%y-%m-%d"),
        starship_data.url,
    ]

    starship_id = int(starship_data.url.split("/")[-2])

    result = insert_resource(
        "starship", "starship_id", starship_id, starship_columns, starship_values
    )

    if result:
        msg = "Record Created Successfully"
    else:
        response = {"message": "Record already inserted"}

        return Response(json.dumps(response), status=409, mimetype="application/json")
    response_obj = {
        "Record_Count": result,
        "Name": starship_data.name,
        "Message": msg,
    }

    ResponseValidation(**response_obj)

    return Response(json.dumps(response_obj), status=201, mimetype="application/json")


@starships_app.route("/starship", methods=["DELETE"])
def delete_starship_data():
    starship_id = request.args.get("starship_id")
    result = __delete_resource("starship", "starship_id", starship_id)

    if result == 0:
        return abort(400)

    response_obj = {
        "Message": f"[ INFO ] Record against starship_id {starship_id} deleted successfully"
    }
    return Response(json.dumps(response_obj), status=200, mimetype="application/json")


@starships_app.route("/starship", methods=["PUT"])
def put_starship_data():
    starship_ = request.json
    try:
        starship_data = Starships(**starship_)
    except pydantic.error_wrappers.ValidationError as ex:
        logging.error(f"{abort(400)} - {ex}")

    url = starship_data.url

    result = upsert_starships(starship_data, url)

    if result:
        msg = "New Record Created Successfully"
    else:
        msg = "Existing record updated successfully"

    response_data = {"Record_Count": result, "Name": starship_data.name, "Message": msg}
    ResponseValidation(**response_data)

    return Response(json.dumps(response_data), status=200, mimetype="application/json")


@starships_app.route("/starship", methods=["PATCH"])
def patch_starship_data():
    starship_ = request.json

    try:
        starship_data = PatchStarship(**starship_)
    except pydantic.error_wrappers.ValidationError as ex:
        return abort(400) - ex

    url = starship_data.url
    result = upsert_starships(starship_data, url)

    if result:
        msg = "New Record Created Successfully"
    else:
        msg = "Existing Record Updated Successfully"

    response_obj = {
        "Record_Count": result,
        "Name": starship_data.name,
        "Message": msg
    }

    ResponseValidation(**response_obj)

    return Response(
        json.dumps(response_obj),
        status=200,
        mimetype="application/json"
    )
