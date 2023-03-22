from pydantic import parse_obj_as
from typing import List
import pydantic.error_wrappers
from models.datamodels.species import Species, PatchSpecie
from dal.dml import insert_resource, upsert_species, fetch_resource, __delete_resource
from response_validation.response import ResponseValidation
from flask import Blueprint, Response, request, abort
import json
import logging


species_app = Blueprint("species", __name__, url_prefix="/api")


@species_app.route("/species", methods=["GET"])
def get_species():
    data = fetch_resource("species")
    species = data.get("results")
    species_ = parse_obj_as(List[Species], species)
    species_data = []
    for specie in species_:
        specie = Species(**dict(specie))
        data = specie.json()
        species_data.append(data)
    return Response(json.dumps(species_data), status=200, mimetype="application/json")


@species_app.route("/specie", methods=["POST"])
def post_specie_data():
    specie_ = request.json
    try:
        specie_data = Species(**specie_)
    except pydantic.error_wrappers.ValidationError as ex:
        response_obj = {"Message": f"{ex}"}
        return Response(
            json.dumps(response_obj), status=422, mimetype="application/json"
        )
    specie_columns = [
        "name",
        "classification",
        "designation",
        "average_height",
        "skin_colors",
        "hair_colors",
        "eye_colors",
        "average_lifespan",
        "homeworld",
        "language",
        "created",
        "edited",
        "url",
    ]

    specie_values = [
        specie_data.name,
        specie_data.classification,
        specie_data.designation,
        specie_data.average_height,
        specie_data.skin_colors,
        specie_data.hair_colors,
        specie_data.eye_colors,
        specie_data.average_lifespan,
        specie_data.homeworld,
        specie_data.language,
        specie_data.created.strftime("%y-%m-%d"),
        specie_data.edited.strftime("%y-%m-%d"),
        specie_data.url,
    ]

    specie_id = int(specie_data.url.split("/")[-2])

    result = insert_resource(
        "species", "species_id", specie_id, specie_columns, specie_values
    )

    if result:
        msg = "Record Created Successfully"
    else:
        response = {"message": "Record already inserted"}

        return Response(json.dumps(response), status=409, mimetype="application/json")
    response_obj = {
        "Record_Count": result,
        "Name": specie_data.name,
        "Message": msg,
    }

    ResponseValidation(**response_obj)

    return Response(json.dumps(response_obj), status=201, mimetype="application/json")


@species_app.route("/specie", methods=["DELETE"])
def delete_specie_data():
    specie_id = request.args.get("specie_id")
    result = __delete_resource("species", "species_id", specie_id)

    if result == 0:
        return abort(400)

    response_obj = {
        "Message": f"[ INFO ] Record against specie id {specie_id} deleted successfully"
    }
    return Response(json.dumps(response_obj), status=200, mimetype="application/json")


@species_app.route("/specie", methods=["PUT"])
def put_specie_data():
    specie_ = request.json
    try:
        specie_data = Species(**specie_)
    except pydantic.error_wrappers.ValidationError as ex:
        logging.error(f"{abort(400)} - {ex}")

    url = specie_data.url.split("/")[-2]

    result = upsert_species(specie_data, url)

    if result:
        msg = "New Record Created Successfully"
    else:
        msg = "Existing record updated successfully"

    response_data = {"Record_Count": result, "Name": specie_data.name, "Message": msg}
    ResponseValidation(**response_data)

    return Response(json.dumps(response_data), status=200, mimetype="application/json")


@species_app.route("/specie", methods=["PATCH"])
def patch_specie_data():
    specie_ = request.json

    try:
        specie_data = PatchSpecie(**specie_)
    except pydantic.error_wrappers.ValidationError as ex:
        return abort(400) - ex

    url = specie_data.url.split("/")[-2]
    result = upsert_species(specie_data, url)

    if result:
        msg = "New Record Created Successfully"
    else:
        msg = "Existing Record Updated Successfully"

    response_obj = {
        "Record_Count": result,
        "Name": specie_data.name,
        "Message": msg
    }

    ResponseValidation(**response_obj)

    return Response(
        json.dumps(response_obj),
        status=200,
        mimetype="application/json"
    )
