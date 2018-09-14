# ---- Base python ----
FROM python:3.6.1-alpine3.6 as base
# Create app directory
WORKDIR /app

# ---- Dependencies ----
FROM base AS dependencies
RUN apk update && \
    apk add postgresql-dev gcc python3-dev musl-dev libffi-dev make && \
    pip install psycopg2
COPY requirements/requirements.txt ./
# install app dependencies
RUN pip install -r requirements.txt

# ---- Copy Files/Build ----
FROM dependencies AS build
WORKDIR /app
COPY api /app/api
COPY wsgi.py /app/.
COPY migrations /app/migrations

# --- Release with Alpine ----
FROM python:3.6.1-alpine3.6 AS release
RUN apk add --no-cache curl pkgconfig openssl-dev libffi-dev musl-dev make gcc krb5-dev
# Create app directory
WORKDIR /app

COPY --from=dependencies /app/requirements.txt ./
COPY --from=dependencies /root/.cache /root/.cache

# Install app dependencies
RUN pip install -r requirements.txt
COPY --from=build /app/ ./

EXPOSE 4009

CMD ["sh", "-c", "flask deploy && gunicorn -b 0.0.0.0:4009 wsgi"]
