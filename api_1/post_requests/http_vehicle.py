import pydantic.error_wrappers

import pydantic.error_wrappers
from flask import Blueprint, Response, request
from resources.people import fetch_resource
from models.datamodels.vehicles import Vehicles
from pydantic import parse_obj_as
from typing import List
from dal.dml import insert_resource
import json
from response_validation.response import PostResponse


vehicle_api = Blueprint("vehicles", __name__, url_prefix="/api/vehicles")


@vehicle_api.route("/get_vehicles", methods=["GET"])
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


@vehicle_api.route("/post_vehicle", methods=["POST"])
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

    PostResponse(**response_obj)

    return Response(json.dumps(response_obj), status=201, mimetype="application/json")
