import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))

import base64
import flask_restful
import json
import mock
import pytest
import restcar

from flask import url_for
from restcar.models import User
from restcar.extensions import db


TEST_EMAIL = 'a@b.com'
TEST_PASSWORD = '123'


def do_not_save(o):
    return o


def get_default_user(email):
    return User(email=email, password=TEST_PASSWORD)


def get_active_user(email):
    return User(email=email, password=TEST_PASSWORD, active=True)


@pytest.fixture
def active_user(request):
    user = get_active_user(TEST_EMAIL)
    def fin():
        db.session.delete(user)
        db.session.commit()
    request.addfinalizer(fin)

    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def inactive_user(request):
    user = get_active_user(TEST_EMAIL)
    user.active = False
    def fin():
        db.session.delete(user)
        db.session.commit()
    request.addfinalizer(fin)

    db.session.add(user)
    db.session.commit()
    return user


def test_createuser(client, monkeypatch):
    sample_email = b'a@b.com'

    monkeypatch.setattr(restcar.extensions.db.session, 'add', do_not_save)

    response = client.post(url_for('api.userresource'), data={'email':sample_email, 'password': TEST_PASSWORD})
    assert response.status_code == 200
    assert b'check your e-mail for the activation link' in response.data
    assert sample_email in response.data


def test_activate_user(client, monkeypatch):
    monkeypatch.setattr(restcar.extensions.db.session, 'add', do_not_save)
    monkeypatch.setattr(restcar.models.User, 'get_by_email', get_default_user)

    response = client.get(url_for('api.useractivationresource', email=TEST_EMAIL))
    assert b'activated successfully' in response.data


def test_already_active(client, monkeypatch):
    monkeypatch.setattr(restcar.extensions.db.session, 'add', do_not_save)
    monkeypatch.setattr(restcar.models.User, 'get_by_email', get_active_user)

    response = client.get(url_for('api.useractivationresource', email=TEST_EMAIL))
    assert b'already active' in response.data


def test_forbidden(client):
    response = client.get(url_for('api.restrictedresource'))
    assert response.status_code == 401


def test_logged_allowed(client, active_user):
    credentials = base64.b64encode(bytes('{}:{}'.format(TEST_EMAIL, TEST_PASSWORD), 'utf-8')).decode('utf-8')
    response = client.get(
        url_for('api.restrictedresource'),
        headers={'Authorization': 'Basic ' + credentials})
    assert response.status_code == 200
    assert b'You shall pass!' in response.data


def test_inactive_restricted(client, inactive_user):
    credentials = base64.b64encode(bytes('{}:{}'.format(TEST_EMAIL, TEST_PASSWORD), 'utf-8')).decode('utf-8')
    response = client.get(
        url_for('api.restrictedresource'),
        headers={'Authorization': 'Basic ' + credentials})
    assert response.status_code == 401
