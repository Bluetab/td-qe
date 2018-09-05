FROM python:3.6.1-alpine3.6 as base

FROM base as builder

MAINTAINER The True-Dat Dev Team

RUN apk update && \
    apk add postgresql-dev gcc python3-dev musl-dev libffi-dev make && \
    pip install psycopg2

RUN mkdir -p /install
COPY . /install
WORKDIR /install

RUN pip install -e .

FROM base

COPY --from=builder /install /usr
COPY . /app
WORKDIR /app

CMD ["python","run.py"]
