FROM python:3.8-slim

WORKDIR /app

# Copy source code.
COPY . /app/
COPY ./requirements.txt /app/requirements.txt

# Install requirements and delete pip cache.
RUN pip install -r /app/requirements.txt \
    && rm -rf /root/.cache/pip
