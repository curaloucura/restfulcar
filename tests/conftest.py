import pytest
import os
from restcar import create_app, db
from restcar import models


@pytest.fixture
def app():
    app = create_app()
    db.create_all()
    db.session.commit()
    return app