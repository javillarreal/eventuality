# eventuality

Prerequisites
- Docker
- docker-compose

Commands to run:
- docker-compose build
- docker-compose up -d

## Database commands
### Should be managed by docker itself (issue):
(in docker db container):
- psql -U postgres
- CREATE USER <username> WITH PASSWORD '<password>';
- CREATE DATABASE <database> OWNER <username>;

Create database for fisrt time (in docker web container):
- python manage.py create-db

Load initial data:
- python manage.py seed-db

Migrate database:
- flask db migrate -m "optional message"
- flask upgrade
