#!/usr/bin/env python

'''The demo module, containing the app factory function.'''

import logging
import os
import sys

from flask import Flask

from restcar.extensions import db, auth, migrate
from restcar.models import User
from restcar.resources import api_blueprint
from restcar.settings import LiveConfig, DevConfig, TestConfig


configs = {
    'live': LiveConfig,
    'dev': DevConfig,
    'test': TestConfig,
}

DefaultConfig = configs.get(os.getenv("FLASK_ENV"), DevConfig)


def create_app(config_object=DefaultConfig):
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app):
    app.register_blueprint(api_blueprint)


@auth.verify_password
def verify_pw(username, password):
    """
    Global Basic Auth login check
    """
    if not username:
        return False

    user = User.get_by_email(username)
    if (not user) or (not user.active):
        return False

    return user.check_password(password)
