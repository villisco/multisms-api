ARG ARTIFACTORY_URL
FROM $ARTIFACTORY_URL/docker-hub/library/python:3.13-alpine

ENV TZ=Europe/Tallinn

COPY src .

RUN pip3 install -r requirements.txt

# Using Gunicorn WSGI server for production
# - multiple workers supported
# - hardened for production
# - no dev only features (debugger/reloader)
CMD [ "gunicorn", "--config", "gunicorn_config.py", "app:create_app()" ]