from flask import Blueprint, Response
from dal.dml import fetch_resource
from models.datamodels.films import Films
from models.datamodels.characters import Characters
from models.datamodels.planets import Planets
from models.datamodels.species import Species
from models.datamodels.starships import Starships
from models.datamodels.vehicles import Vehicles
from pydantic import parse_obj_as
from typing import List
import json


get_endpoint = Blueprint("get_request", __name__, url_prefix="/api")


@get_endpoint.route("/films", methods=["GET"])
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


@get_endpoint.route("/characters", methods=["GET"])
def get_characters():
    data = fetch_resource("people")
    characters = data.get("results")
    characters_ = parse_obj_as(List[Characters], characters)
    characters_data = []
    for character in characters_:
        character = Characters(**dict(character))
        data = character.json()
        characters_data.append(data)
    return Response(
        json.dumps(characters_data), status=200, mimetype="application/json"
    )


@get_endpoint.route("/planets", methods=["GET"])
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


@get_endpoint.route("/species", methods=["GET"])
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


@get_endpoint.route("/starships", methods=["GET"])
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


@get_endpoint.route("/vehicles", methods=["GET"])
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
