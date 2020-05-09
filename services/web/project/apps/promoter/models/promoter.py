from project.app import db


users = Table('users',
    db.Column('promoter_id', db.Integer, db.ForeignKey('promoter.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('role', db.Integer, nullable=False)
)


class Promoter(db.Model):
    ROLES = {
        'support': 0,
        'creator': 1,
        'admin': 2
    }

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.String)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.now)
    longitude = db.Column(db.Float(precision=9))
    latitude = db.Column(db.Float(precision=9))
    email = db.Column(db.String(40), unique=True)
    main_category = db.Column(db.Integer, db.ForeignKey('event_category.id'), nullable=True)
    users = db.relationship('User', secondary=users, lazy='subquery', backref=db.backref('pages', lazy=True))

    def __repr__(self):
        return f'<Promoter: {self.name}>'
