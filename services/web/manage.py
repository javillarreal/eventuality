import json

import click
from flask.cli import FlaskGroup

import spotipy
from project import settings
from project.app import EventCategory, User, app, db
from spotipy.oauth2 import SpotifyClientCredentials

cli = FlaskGroup(app)


@cli.command('create-db')
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command('seed-db')
def seed_db():
    # load initial event categories
    print('Loading data file')
    categories_file = 'data.json'
    with open(categories_file, 'r') as file:
        categories = json.load(file)
    categories = categories['categories']

    print('Adding new categories')
    for category_dict in categories:
        print(category_dict)
        db.session.add(EventCategory(**category_dict))
    db.session.commit()
    print('Categories added')

    # music_category = EventCategory.query.filter(EventCategory.name=='Music').first()
    #  
    # print('Fetching music subcategories form spotify')
    # sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
    #     client_id=settings.spotify['SPOTIFY_CLIENT_ID'],
    #     client_secret=settings.spotify['SPOTIFY_CLIENT_SECRET']
    # ))
    #
    # result = sp.recommendation_genre_seeds()
    # for genre in result['genres']:
    #     print(genre)
    #     category = EventCategory(
    #         name=genre,
    #         description=f'Main topic of this event: {genre}. Subcategory of: Music'
    #     )
    #     music_category.children.append(category)
    # db.session.commit()
    # print('Music subcategories added')


@cli.command('create-admin')
@click.argument('username')
@click.argument('email')
def create_admin(username, email):
    password = click.prompt('Please enter a secure password', type=str)
    db.session.add(User(
        username=username,
        email=email,
        password=password,
        is_admin=True
    ))
    
    db.session.commit()


if __name__ == '__main__':
    cli()
