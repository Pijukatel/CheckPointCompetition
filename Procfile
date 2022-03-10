release: python ./manage.py migrate
release: python ./manage.py setup_demo
web: gunicorn --pythonpath CheckPointCompetition CheckPointCompetition.wsgi --log-file -
