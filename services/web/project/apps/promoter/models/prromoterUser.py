from project.app import db


class PromoterUser(db.Model):
    USER_ROLES = {
        'support': 0,
        'creator': 1,
        'admin': 2
    }

    promoter_id = db.Column(db.Integer, db.ForeignKey('promoter.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    role = db.Column(db.Integer, default=1, nullable=False)

    promoters = db.relationship('Promoter', backref=db.backref('users'))
    users = db.relationship('User', backref=db.backref('promoters'))
