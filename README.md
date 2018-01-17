Sample RESTful API
==================

Installation
------------

This demo requires Python 3 to make sure to use only the latest Pytest plugins.


If you have a Make environment available, the following commands can be triggered in sequence to get a fully functional test environment:

	# make install
	# make run
	# make test

Manual installation as follows:

	# virtualenv -p python3 venv
	# source venv/bin/activate
	# pip install -r requirements.txt
	# export FLASK_ENV=test; python manage.py test
	# export FLASK_ENV=dev; python manage.py db upgrade
	# export FLASK_ENV=dev; python manage.py server


API Endpoints
-------------

(Also available as swagger file in the repository)

Create a new user
POST /api/v1/users/
data: email, password

Activate a new user (hash instead of plain email would be safer, but it requires more development time)
GET /api/v1/<email>/activate

Protected resource
GET /api/v1/restricted


Deployment
----------

gunicorn config file is available that could be hooked up with supervisor and Nginx


Tests
-----

Pytests are included. They cover all basic functions of the API as such creating user and accessing restricted content.