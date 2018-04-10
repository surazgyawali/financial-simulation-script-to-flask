run:
	export FLASK_APP=game.py; flask run

debug:
	export FLASK_APP=game.py; FLASK_DEBUG=1 flask run
