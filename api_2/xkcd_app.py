from flask import Blueprint

xkcd_api = Blueprint("xkcd", __name__, url_prefix="/api/xkcd")


@xkcd_api.route("/welcome")
def welcome():
    return "This message is coming from xkcd api"


@xkcd_api.route("/")
def hi_all():
    return f"<h1> Hi all from xkcd </h1>"
