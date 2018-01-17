# -*- coding: utf-8 -*-
from flask_migrate import Migrate
migrate = Migrate()

from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
