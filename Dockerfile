# ---- Base python ----
FROM python:3.6.1-alpine3.6 as base
# Create app directory
WORKDIR /app

# ---- Dependencies ----
FROM base AS dependencies
RUN apk update && \
    apk add --no-cache postgresql-dev gcc python3-dev musl-dev libffi-dev make libpq && \
    pip install --upgrade pip && pip install psycopg2
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
RUN apk add --no-cache python3-dev curl pkgconfig openssl-dev libffi-dev musl-dev make gcc krb5-dev libpq
# Create app directory
WORKDIR /app

COPY --from=dependencies /app/requirements.txt ./
COPY --from=dependencies /root/.cache /root/.cache

# Install app dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY --from=build /app/ ./

EXPOSE 4009

ENTRYPOINT ["sh", "-c", "APP_ENV=Production flask deploy && APP_ENV=Production gunicorn -b 0.0.0.0:4009 wsgi"]
