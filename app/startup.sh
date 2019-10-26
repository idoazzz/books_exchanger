# pipenv run alembic -c ./db/alembic.ini stamp head
# pipenv run alembic -c ./db/alembic.ini revision --autogenerate -m "First migration."
pipenv run alembic -c ./db/alembic.ini upgrade head
uvicorn main:app --host 0.0.0.0 --port 8080 --reload