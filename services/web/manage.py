import click
from flask.cli import FlaskGroup

from project.app import app, db, EventCategory, User

cli = FlaskGroup(app)

@cli.command('create-db')
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command('seed-db')
def seed_db():
    # just dummy categories
    db.session.add(EventCategory(
        name='Music',
        description='Main category of this event is: music',
        default=False
    ))
    db.session.add(EventCategory(
        name='Other',
        description='Main category of this event is: other',
        default=True
    ))
    
    # first admin
    db.session.add(User(
        username='jaimescose',
        email='jaimescoseru@gmail.com',
        is_admin=True
    ))

    db.session.commit()


@cli.command('create-admin')
@click.argument('username')
@click.argument('email')
def create_admin(username, email):
    password = click.prompt('Please enter a secur password', type=str)
    db.session.add(User(
        username=username,
        email=email,
        password=password,
        is_admin=True
    ))
    
    db.session.commit()

if __name__ == '__main__':
    cli()
