FROM python:3.7

COPY . /

RUN pip install pipenv

WORKDIR /app

RUN pipenv install --system

EXPOSE 8080

ENTRYPOINT ["/bin/bash", "startup.sh"]