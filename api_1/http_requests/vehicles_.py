from pydantic import parse_obj_as
from typing import List
import pydantic.error_wrappers
from models.datamodels.vehicles import Vehicles, PatchVehicle
from dal.dml import insert_resource, upsert_vehicles, fetch_resource, __delete_resource
from response_validation.response import ResponseValidation
from flask import Blueprint, Response, request, abort
import json
import logging


vehicles_app = Blueprint("vehicles", __name__, url_prefix="/api")


@vehicles_app.route("/vehicles", methods=["GET"])
def get_vehicles():
    data = fetch_resource("vehicles")
    vehicles = data.get("results")
    vehicles_ = parse_obj_as(List[Vehicles], vehicles)
    vehicles_data = []
    for vehicle in vehicles_:
        vehicle = Vehicles(**dict(vehicle))
        data = vehicle.json()
        vehicles_data.append(data)
    return Response(json.dumps(vehicles_data), status=200, mimetype="application/json")


@vehicles_app.route("/vehicle", methods=["POST"])
def post_vehicle_data():
    vehicle_ = request.json
    try:
        vehicle_data = Vehicles(**vehicle_)
    except pydantic.error_wrappers.ValidationError as ex:
        response_obj = {"Message": f"{ex}"}
        return Response(
            json.dumps(response_obj), status=422, mimetype="application/json"
        )

    vehicle_columns = [
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
        "vehicle_class",
        "created",
        "edited",
        "url",
    ]

    vehicle_values = [
        vehicle_data.name,
        vehicle_data.model,
        vehicle_data.manufacturer,
        vehicle_data.cost_in_credits,
        vehicle_data.length,
        vehicle_data.max_atmosphering_speed,
        vehicle_data.crew,
        vehicle_data.passengers,
        vehicle_data.cargo_capacity,
        vehicle_data.consumables,
        vehicle_data.vehicle_class,
        vehicle_data.created.strftime("%y-%m-%d"),
        vehicle_data.edited.strftime("%y-%m-%d"),
        vehicle_data.url,
    ]

    vehicle_id = int(vehicle_data.url.split("/")[-2])

    result = insert_resource(
        "vehicle", "vehicle_id", vehicle_id, vehicle_columns, vehicle_values
    )

    if result:
        msg = "Record Created Successfully"
    else:
        response = {"message": "Record already inserted"}

        return Response(json.dumps(response), status=409, mimetype="application/json")
    response_obj = {
        "Record_Count": result,
        "Name": vehicle_data.name,
        "Message": msg,
    }

    ResponseValidation(**response_obj)

    return Response(json.dumps(response_obj), status=201, mimetype="application/json")


@vehicles_app.route("/vehicle", methods=["DELETE"])
def delete_vehicle_data():
    vehicle_id = request.args.get("vehicle_id")
    result = __delete_resource("vehicle", "vehicle_id", vehicle_id)

    if result == 0:
        return abort(400)

    response_obj = {
        "Message": f"[ INFO ] Record against vehicle_id {vehicle_id} deleted successfully"
    }
    return Response(json.dumps(response_obj), status=200, mimetype="application/json")


@vehicles_app.route("/vehicle", methods=["PUT"])
def put_vehicle_data():
    vehicle_ = request.json
    try:
        vehicle_data = Vehicles(**vehicle_)
    except pydantic.error_wrappers.ValidationError as ex:
        logging.error(f"{abort(400)} - {ex}")

    url = vehicle_data.url

    result = upsert_vehicles(vehicle_data, url)

    if result:
        msg = "New Record Created Successfully"
    else:
        msg = "Existing record updated successfully"

    response_data = {"Record_Count": result, "Name": vehicle_data.name, "Message": msg}
    ResponseValidation(**response_data)

    return Response(json.dumps(response_data), status=200, mimetype="application/json")


@vehicles_app.route("/vehicle", methods=["PATCH"])
def patch_vehicle_data():
    vehicle_ = request.json

    try:
        vehicle_data = PatchVehicle(**vehicle_)
    except pydantic.error_wrappers.ValidationError as ex:
        return abort(400) - ex

    url = vehicle_data.url
    result = upsert_vehicles(vehicle_data, url)

    if result:
        msg = "New Record Created Successfully"
    else:
        msg = "Existing Record Updated Successfully"

    response_obj = {
        "Record_Count": result,
        "Name": vehicle_data.name,
        "Message": msg
    }

    ResponseValidation(**response_obj)

    return Response(
        json.dumps(response_obj),
        status=200,
        mimetype="application/json"
    )
