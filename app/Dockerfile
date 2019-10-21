FROM python:3.7

COPY . /

RUN pip install pipenv

WORKDIR /app

RUN pipenv install --system

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]