import pydantic.error_wrappers

import pydantic.error_wrappers
from flask import Blueprint, Response, request
from resources.people import fetch_resource
from models.datamodels.films import Films
from pydantic import parse_obj_as
from typing import List
from dal.dml import insert_resource
import json
from response_validation.response import PostResponse


film_api = Blueprint("films", __name__, url_prefix="/api/films")


@film_api.route("/get_films", methods=["GET"])
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


@film_api.route("/post_film", methods=["POST"])
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

    PostResponse(**response_obj)

    return Response(json.dumps(response_obj), status=201, mimetype="application/json")
