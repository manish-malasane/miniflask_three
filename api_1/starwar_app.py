from flask import Blueprint
from dal.people import fetch_resource
from models.datamodels.characters import Characters
from pydantic import parse_obj_as
from typing import List

starwar_api = Blueprint("starwars", __name__, url_prefix="/api/starwars")


@starwar_api.route("/welcome")
def welcome():
    return "Hi this message coming from starwar app"


@starwar_api.route("/")
def hi_all():
    return f"<h1> Hi all from starwars </h1>"


@starwar_api.route("/people")
def get_char():
    data = fetch_resource("people")
    chars = data.get("results")
    new = parse_obj_as(List[Characters], chars)
    return new

