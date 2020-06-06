from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt_claims, verify_jwt_in_request

from project.app import jwt
from project.utils.auth.exceptions import AdminLevelRequired


@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    from project.apps.promoter.models.promoterUser import PromoterUser
    from project.apps.user.models.user import User

    claims = {
        'roles': list(),
        'is_admin': False
    }

    promoter_user_role = PromoterUser.query.filter(PromoterUser.user_id==identity)
    if promoter_user_role:
        claims['roles'] = [r.role for r in promoter_user_role]

    user = User.query.get(identity)
    if user:
        claims['is_admin'] = user.is_admin

    return claims


def admin_required(fn, exception=AdminLevelRequired):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()

        if not claims['is_admin']:
            raise exception
        
        return fn(*args, **kwargs)
    return wrapper


def role_required(fn, role):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        # TODO: implement user role required
    return wrapper
