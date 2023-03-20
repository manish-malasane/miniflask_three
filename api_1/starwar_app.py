from flask import Blueprint
from api_1.http_requests.delete_ import delete_endpoint
from api_1.http_requests.get_ import get_endpoint
from api_1.http_requests.post_ import post_endpoint

starwar_api_ = Blueprint("starwars", __name__)

starwar_api_.register_blueprint(get_endpoint)
starwar_api_.register_blueprint(post_endpoint)
starwar_api_.register_blueprint(delete_endpoint)


@starwar_api_.route("/welcome")
def welcome():
    return "Hi this message coming from starwar app"


@starwar_api_.route("/")
def hi_all():
    return f"<h1> Hi all from starwars </h1>"
