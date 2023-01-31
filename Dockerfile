FROM python:3.11-slim

COPY . /app
WORKDIR /app

RUN  pip install pipenv  \
    && pipenv install
ENV HOST=0.0.0.0
EXPOSE 5000

CMD ["pipenv", "run", "dev"]