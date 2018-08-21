from flask import Flask, Blueprint
from app.index.controller import index_blueprint
app = Flask(__name__)
app.debug = True

app.register_blueprint(index_blueprint)
