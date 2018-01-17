from flask import Flask
from flask_httpauth import HTTPBasicAuth
from flask_migrate import Migrate
from flask_restplus import Resource, Api
from flask_sqlalchemy import SQLAlchemy

from restcar import create_app

app = create_app()

migrate = Migrate()
auth = HTTPBasicAuth()
db = SQLAlchemy(app)
