import pydantic.error_wrappers

import pydantic.error_wrappers
from flask import Blueprint, Response, request
from models.datamodels.films import Films
from models.datamodels.characters import Characters
from models.datamodels.planets import Planets
from models.datamodels.species import Species
from models.datamodels.starships import Starships
from models.datamodels.vehicles import Vehicles
from dal.dml import insert_resource
import json
from response_validation.response import PostResponse


post_endpoint = Blueprint("post_request", __name__, url_prefix="/api")


@post_endpoint.route("/film", methods=["POST"])
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


@post_endpoint.route("/character", methods=["POST"])
def post_char_data():
    character_ = request.json
    try:
        char_data = Characters(**character_)
    except pydantic.error_wrappers.ValidationError as ex:
        response_obj = {"message": f"{ex}"}
        return Response(
            json.dumps(response_obj), status=422, mimetype="application/json"
        )

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
    char_id = int(char_data.url.split("/")[-2])
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

    PostResponse(**response_obj)

    return Response(json.dumps(response_obj), status=201, mimetype="application/json")


@post_endpoint.route("/planet", methods=["POST"])
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


@post_endpoint.route("/specie", methods=["POST"])
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

    PostResponse(**response_obj)

    return Response(json.dumps(response_obj), status=201, mimetype="application/json")


@post_endpoint.route("/starship", methods=["POST"])
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

    PostResponse(**response_obj)

    return Response(json.dumps(response_obj), status=201, mimetype="application/json")


@post_endpoint.route("/vehicle", methods=["POST"])
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
