# alembic -c ./db/alembic.ini stamp head
# alembic -c ./db/alembic.ini revision --autogenerate -m "Changes password length."
# alembic -c ./db/alembic.ini upgrade head
uvicorn main:app --host 0.0.0.0 --port 8080 --reload