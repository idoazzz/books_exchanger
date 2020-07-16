FROM python:3.7

COPY . /

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 8080

ENV PYTHONPATH="/"

ENTRYPOINT ["/bin/bash", "startup.sh"]