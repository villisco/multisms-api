# CHANGELOG

## 3.1.0
- [ui] swagger button added
- [ui] `Receiver Groups` table added separate group `Name` & `Description` columns
- [api] merged `/api/v1/groups` & `/api/v1/config` endpoints into single `/api/v1/config` endpoint
- [python] upgraded `pytest-cov` from `6.3.0` to `7.0.0`

## 3.0.0
- [ui] Application `GET /` now renders "__Current configuration__" view (xhtml template)
- [api] Moved health endpoint from `/` to `/api/v1/health`
- [api] Added new `GET /api/v1/config` endpoint to get envvars list used in xhtml template
- [swagger] config related endpoints now use `Monitoring` tag

## 2.0.0
- More explicit `receiver_groups` configuration  
  __now:__
  ```
  - name: myapp_users_test
    description: TEST myapp alert receivers
    receivers:
      - number: '37258000001'
        name: 'User1'
      - number: '37258000002'
        name: 'User2'
  ```
  before:
  ```
  - name: myapp_users_test
    description: TEST myapp alert receivers
    receivers:
      - '37258000001' # User1
      - '37258000002'
  ```

## 1.2.0
- Added `GET /api/v1/groups` endpoint for checking what `receiver_groups` config app uses

## 1.1.0
- Added __non-root__ user (10001) to `Dockerfile` for app running
- Set `Dockerfile` `WORKDIR` to `/app`
- Added `.dockerignore` to exclude tests/junk from `Dockerfile` `COPY` command
- Updated `requests` package v2.32.4->__v2.32.5__
- Updated `flask-openapi3-swagger`package v5.27.1->__v5.28.0__

## 1.0.0
- initial version of the application