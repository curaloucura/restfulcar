test:
	export FLASK_ENV=test; venv/bin/python manage.py test

install:
	virtualenv -p python3 venv
	venv/bin/pip install -r requirements.txt
	export FLASK_ENV=dev; venv/bin/python manage.py db upgrade

server:
	export FLASK_ENV=dev; venv/bin/python manage.py server

.PHONY: test install server
