#!/usr/bin/env python

from flask_script import Manager, Server
from flask_migrate import MigrateCommand

from restcar.models import User
from restcar import create_app
from restcar.extensions import db


app = create_app()
manager = Manager(app)


@manager.command
def test():
    """Run the tests."""
    import pytest
    import os
    os.environ['FLASK_ENV'] = 'test'
    exit_code = pytest.main(['tests', '-q'])
    return exit_code


manager.add_command('server', Server())
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()