from flask import Flask
from api_1.starwar_app import starwar_api
from api_2.xkcd_app import xkcd_api

app = Flask(__name__)

app.register_blueprint(starwar_api)
app.register_blueprint(xkcd_api)

