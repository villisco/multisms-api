# CHANGELOG

## 1.0.0
- initial version of the application

## 1.1.0
- Added __non-root__ user (10001) to `Dockerfile` for app running
- Set `Dockerfile` `WORKDIR` to `/app`
- Added `.dockerignore` to exclude tests/junk from `Dockerfile` `COPY` command
- Updated `requests` package v2.32.4->__v2.32.5__
- Updated `flask-openapi3-swagger`package v5.27.1->__v5.28.0__
- Added K8S deployment example (helm-chart) to `k8s/helm-chart`

## 1.2.0
- Added `GET /api/v1/groups` endpoint for checking what `receiver_groups` config app uses
- Fix `k8s/helm-chart` missing `description` field in `receiver_groups` config template

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