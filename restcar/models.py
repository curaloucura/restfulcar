import logging
from flask import url_for, request
from werkzeug.security import generate_password_hash, check_password_hash

from restcar.extensions import db

logger = logging.getLogger()

class User(db.Model):
    __tablename__ = 'users'
    email = db.Column(db.String, primary_key=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    active = db.Column(db.Boolean, default=False)

    def __init__(self, email, password, **kwargs):
        db.Model.__init__(self, email=email,
                          password=password, **kwargs)
        self.set_password(password)

    def __repr__(self):  # pragma: nocover
        return '<User({email})>'.format(email=self.email)

    @property
    def password(self):
        return None

    @password.setter
    def password(self, password):
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, value):
        return check_password_hash(self.password_hash, value)

    def activate(self):
        self.active = True
        db.session.add(self)
        db.session.commit()

    def send_activation_email(self):
        url = url_for('api.useractivationresource', email=self.email)
        url = request.url_root+url[1:]
        msg = """
        Thank you for signing up.
        Before you can use our API, please activate your account by visiting the link below:

        {}

        Cheers,
        Your Team
        """.format(url)

        # TODO: setting logger to ERROR to avoid extra log configuration for this task in order to print it
        logger.error(msg)

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
