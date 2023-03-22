from flask import Blueprint
from api_1.http_requests.characters_ import characters_app
from api_1.http_requests.films_ import film_app
from api_1.http_requests.planets_ import planets_app
from api_1.http_requests.vehicles_ import vehicles_app
from api_1.http_requests.starships_ import starships_app
from api_1.http_requests.species_ import species_app

starwar_api_ = Blueprint("starwars", __name__)

starwar_api_.register_blueprint(vehicles_app)
starwar_api_.register_blueprint(planets_app)
starwar_api_.register_blueprint(characters_app)
starwar_api_.register_blueprint(starships_app)
starwar_api_.register_blueprint(film_app)
starwar_api_.register_blueprint(species_app)


@starwar_api_.route("/welcome")
def welcome():
    return "Hi this message coming from starwar app"


@starwar_api_.route("/")
def hi_all():
    return f"<h1> Hi all from starwars </h1>"
