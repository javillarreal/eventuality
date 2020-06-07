# eventuality

Prerequisites
- Docker
- docker-compose

Commands to run:
- docker-compose build
- docker-compose up -d

## Database commands
Create database for fisrt time (in docker web container):
- python manage.py create-db

Load initial data:
- python manage.py

Migrate database:
- flask db migrate -m "optional message"
- flask upgrade
