import logging

from pydantic import parse_obj_as
from typing import List
import pydantic.error_wrappers
from models.datamodels.films import Films, PatchFilm
from dal.dml import insert_resource, __delete_resource, fetch_resource, upsert_films
from response_validation.response import ResponseValidation
from flask import Blueprint, Response, request, abort
import json


film_app = Blueprint("film", __name__, url_prefix="/api")


@film_app.route("/films", methods=["GET"])
def get_films():
    data = fetch_resource("films")
    films = data.get("results")
    films_ = parse_obj_as(List[Films], films)
    films_data = []
    for film in films_:
        film = Films(**dict(film))
        data = film.json()
        films_data.append(data)
    return Response(json.dumps(films_data), status=200, mimetype="application/json")


@film_app.route("/film", methods=["POST"])
def post_films_data():
    film_ = request.json
    try:
        film_data = Films(**film_)
    except pydantic.error_wrappers.ValidationError as ex:
        response_obj = {"Message": f"{ex}"}
        return Response(
            json.dumps(response_obj), status=422, mimetype="application/json"
        )
    film_columns = [
        "title",
        "episode_id",
        "opening_crawl",
        "director",
        "producer",
        "release_date",
        "created",
        "edited",
        "url",
    ]
    film_values = [
        film_data.title,
        film_data.episode_id,
        film_data.opening_crawl,
        film_data.director,
        film_data.producer,
        film_data.release_date,
        film_data.created.strftime("%y-%m-%d"),
        film_data.edited.strftime("%y-%m-%d"),
        film_data.url,
    ]
    film_id = int(film_data.url.split("/")[-2])
    result = insert_resource("film", "film_id", film_id, film_columns, film_values)

    if result:
        msg = "Record Created Successfully"
    else:
        response = {"message": "Record already inserted"}

        return Response(json.dumps(response), status=409, mimetype="application/json")
    response_obj = {
        "Record_Count": result,
        "Name": film_data.title,
        "Message": msg,
    }

    ResponseValidation(**response_obj)

    return Response(json.dumps(response_obj), status=201, mimetype="application/json")


@film_app.route("/film", methods=["DELETE"])
def delete_film_data():
    film_id = request.args.get("film_id")
    result = __delete_resource("film", "film_id", film_id)

    if result == 0:
        return abort(400)

    response_obj = {
        "Message": f"[ INFO ] Record against film id {film_id} deleted successfully"
    }
    return Response(json.dumps(response_obj), status=200, mimetype="application/json")


@film_app.route("/film", methods=["PUT"])
def put_film_data():
    film_ = request.json
    try:
        film_data = Films(**film_)
    except pydantic.error_wrappers.ValidationError as ex:
        logging.error(f"{abort(400)} - {ex}")

    url = film_data.url.split("/")[-2]

    result = upsert_films(film_data, url)

    if result:
        msg = "New Record Created Successfully"
    else:
        msg = "Existing record updated successfully"

    response_data = {"Record_Count": result, "Name": film_data.title, "Message": msg}
    ResponseValidation(**response_data)

    return Response(json.dumps(response_data), status=200, mimetype="application/json")


@film_app.route("/film", methods=["PATCH"])
def patch_film_data():
    film_ = request.json

    try:
        film_data = PatchFilm(**film_)
    except pydantic.error_wrappers.ValidationError as ex:
        return f"{abort(400)} - {ex}"

    url = film_data.url.split("/")[-2]
    result = upsert_films(film_data, url)

    if result:
        msg = "New Record Created Successfully"
    else:
        msg = "Existing Record Updated Successfully"

    response_obj = {
        "Record_Count": result,
        "Name": film_data.title,
        "Message": msg
    }

    ResponseValidation(**response_obj)

    return Response(
        json.dumps(response_obj),
        status=200,
        mimetype="application/json"
    )
