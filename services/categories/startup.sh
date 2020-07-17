alembic -c app/db/alembic.ini upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

