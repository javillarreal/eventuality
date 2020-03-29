from flask.cli import FlaskGroup

from project import app, db
from project import Category

cli = FlaskGroup(app)

@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command("seed_db")
def seed_db():
    db.session.add(Category(
        name='Music',
        description='Main category of this event is: music',
        default=False
    ))
    db.session.add(Category(
        name='Other',
        description='Main category of this event is: other',
        default=True
    ))
    db.session.commit()

if __name__ == "__main__":
    cli()
