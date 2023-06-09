from pydantic import parse_obj_as
from typing import List
import pydantic.error_wrappers
from models.datamodels.characters import Characters, PatchCharacter
from dal.dml import insert_resource, upsert_characters, fetch_resource, __delete_resource
from response_validation.response import ResponseValidation
from flask import Blueprint, Response, request, abort
import json
import logging


characters_app = Blueprint("characters", __name__, url_prefix="/api")


@characters_app.route("/characters", methods=["GET"])
def get_characters():

    data = fetch_resource("people")   # fetches the resource data from swapi.dev
    characters = data.get("results")   # there are keys we are pulling out data of results keys
    characters_ = parse_obj_as(List[Characters], characters)  # here we, mapping that data as a list of pydantic model
    characters_data = []

    for character in characters_:
        character = Characters(**dict(character))  # character data is serialized with model here we typecast that to dict
        data = character.json()                    # pulling out json data from that
        characters_data.append(data)               # appending that to characters_data list

    return Response(
        json.dumps(characters_data), status=200, mimetype="application/json"
    )                                              # returning response obj


@characters_app.route("/character", methods=["POST"])
def post_char_data():
    character_ = request.json            # capturing the request payload / data

    # REQUEST VALIDATION
    try:
        char_data = Characters(**character_)    # serializing request payload as a json with pydantic model
    except pydantic.error_wrappers.ValidationError as ex:
        response_obj = {"message": f"{ex}"}
        return Response(
            json.dumps(response_obj), status=422, mimetype="application/json"
        )

    # DB COLUMNS
    char_columns = [
        "name",
        "height",
        "mass",
        "hair_color",
        "skin_color",
        "eye_color",
        "birth_year",
        "gender",
        "homeworld",
        "created",
        "edited",
        "url",
    ]

    # DB VALUES WHICH WE HAVE TO PASS AGAINST EACH KEY pulling out from char_data.
    char_values = [
        char_data.name,
        char_data.height,
        char_data.mass,
        char_data.hair_color,
        char_data.skin_color,
        char_data.eye_color,
        char_data.birth_year,
        char_data.gender,
        char_data.homeworld,
        char_data.created.strftime("%y-%m-%d"),
        char_data.edited.strftime("%y-%m-%d"),
        char_data.url,
    ]

    # CAPTURING CHAR ID
    char_id = int(char_data.url.split("/")[-2])

    # INSERTING DATA INTO THE DATABASE
    result = insert_resource(
        "characters", "char_id", char_id, char_columns, char_values
    )

    if result:
        msg = "Record Created Successfully"
    else:
        response_obj = {"msg": "Record already inserted"}
        return Response(
            json.dumps(response_obj), status=409, mimetype="application/json"
        )

    response_obj = {"Record_Count": result, "Name": char_data.name, "Message": msg}

    # RESPONSE BODY VALIDATION
    ResponseValidation(**response_obj)

    return Response(json.dumps(response_obj), status=201, mimetype="application/json")


@characters_app.route("/character", methods=["DELETE"])
def delete_char_data():
    """ BY CAPTURING THE QUERY PARAM"""

    char_id = request.args.get("char_id")           # capturing the passed char id
    result = __delete_resource("characters", "char_id", char_id)

    if result == 0:
        return abort(400)

    response_obj = {
        "Message": f"[ INFO ] Record against film id {char_id} deleted successfully"
    }
    return Response(json.dumps(response_obj), status=200, mimetype="application/json")


@characters_app.route("/character", methods=["PUT"])
def put_character_data():
    character_ = request.json         # CAPTURING THE REQUEST PAYLOAD

    # REQUEST BODY VALIDATION
    try:
        character_data = Characters(**character_)      # SERIALIZE THE DATA WITH PYDANTIC MODEL
    except pydantic.error_wrappers.ValidationError as ex:
        logging.error(f"{abort(400)} - {ex}")

    # PULLING OUT URL FROM serialize data and capturing id
    url = character_data.url

    result = upsert_characters(character_data, url)

    if result:
        msg = "New Record Created Successfully"
    else:
        msg = "Existing record updated successfully"

    response_data = {
        "Record_Count": result,
        "Name": character_data.name,
        "Message": msg,
    }
    ResponseValidation(**response_data)

    return Response(json.dumps(response_data), status=200, mimetype="application/json")


@characters_app.route("/character", methods=["PATCH"])
def patch_char_data():
    char_ = request.json

    try:
        character_data = PatchCharacter(**char_)
    except pydantic.error_wrappers.ValidationError as ex:
        return f"{abort(400)} - {ex}"

    url = character_data.url
    result = upsert_characters(character_data, url)

    if result:
        msg = "New Record Created Successfully"
    else:
        msg = "Existing Record Updated Successfully"

    response_obj = {
        "Record_Count": result,
        "Name": character_data.name,
        "Message": msg
    }

    ResponseValidation(**response_obj)

    return Response(
        json.dumps(response_obj),
        status=200,
        mimetype="application/json"
    )
