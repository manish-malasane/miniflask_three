from flask import Blueprint
from api_1.post_requests.http_film import film_api
from api_1.post_requests.http_planet import planet_api
from api_1.post_requests.http_specie import specie_api
from api_1.post_requests.http_people import character_api
from api_1.post_requests.http_vehicle import vehicle_api
from api_1.post_requests.http_starship import starship_api


starwar_api_ = Blueprint("starwars", __name__)

starwar_api_.register_blueprint(film_api)
starwar_api_.register_blueprint(planet_api)
starwar_api_.register_blueprint(specie_api)
starwar_api_.register_blueprint(character_api)
starwar_api_.register_blueprint(vehicle_api)
starwar_api_.register_blueprint(starship_api)


@starwar_api_.route("/welcome")
def welcome():
    return "Hi this message coming from starwar app"


@starwar_api_.route("/")
def hi_all():
    return f"<h1> Hi all from starwars </h1>"
