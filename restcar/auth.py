#!/usr/bin/env python

import functools
from flask import g, abort
from restcar.extensions import auth
from restcar.models import User


@auth.verify_password
def verify_password(email, password):
    """Validate user passwords and store user in the 'g' object"""
    g.user = User.query.filter_by(email=email).first()
    return g.user is not None and g.user.check_password(password)
