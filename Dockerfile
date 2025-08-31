ARG ARTIFACTORY_URL
FROM $ARTIFACTORY_URL/docker-hub/library/python:3.13-alpine

ENV TZ=Europe/Tallinn

ARG UID=10001
ARG GID=10001

RUN addgroup -g ${GID} -S appgroup \
 && adduser  -u ${UID} -S -G appgroup -h /app -s /sbin/nologin appuser

WORKDIR /app

COPY --chown=${UID}:${GID} src .

# install as root
RUN pip3 install -r requirements.txt

# switch to non-root user
USER ${UID}:${GID}

# Using Gunicorn WSGI server for production
# - multiple workers supported
# - hardened for production
# - no dev only features (debugger/reloader)
CMD [ "gunicorn", "--config", "gunicorn_config.py", "app:create_app()" ]