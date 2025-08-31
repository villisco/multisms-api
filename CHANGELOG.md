# CHANGELOG

## 1.0.0
- initial version of the application

## 1.1.0
- Added __non-root__ user (10001) to `Dockerfile` for app running
- Set `Dockerfile` `WORKDIR` to `/app`
- Added `.dockerignore` to exclude tests/junk from `Dockerfile` `COPY` command
- Updated `requests` package v2.32.4->__v2.32.5__
- Updated `flask-openapi3-swagger`package v5.27.1->__v5.28.0__