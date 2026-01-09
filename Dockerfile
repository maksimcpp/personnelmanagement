FROM python:3.12-slim

WORKDIR /app
COPY . /app

RUN pip3 install -r requirements.txt

WORKDIR /app/src

CMD alembic -c ../alembic.ini upgrade head \
    && python3 app.py
