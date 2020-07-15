from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt_claims, verify_jwt_in_request, get_jwt_identity

from project.app import jwt
from project.utils.auth.exceptions import (AdminLevelRequired,
                                           UserRoleNotSufficed)

from project.apps.user.models.user import User
from project.apps.promoter.models.promoter import Promoter, PromoterUser


@jwt.user_claims_loader
def add_claims_to_access_token(identity):

    claims = {
        'identity': identity,
        'is_admin': False
    }

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


def requires_access_level(required_role: int, exception=UserRoleNotSufficed):
    def decorator(fn):
        @wraps(fn)
        def decorated_function(*args, **kwargs):
            verify_jwt_in_request()
            
            user_id = get_jwt_identity()
            user = User.query.get(user_id)

            main_promoters_ids = kwargs.get('main_promoters_ids')
            
            max_role = PromoterUser.query.filter(
                PromoterUser.user==user,
                PromoterUser.promoter_id.in_(main_promoters_ids)
            ).order_by(PromoterUser.role.desc()).first()

            if max_role is not None:
                if max_role.role >= required_role:
                    return fn(*args, **kwargs)

            raise exception
        
        return decorated_function
    return decorator


def role_required(fn, required_role, exception=UserRoleNotSufficed):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()

        user_roles = claims['roles']
        print(type(user_roles), user_roles)

        print(*args)

        print(**kwargs)
        
        return fn(*args, **kwargs)
    return wrapper
