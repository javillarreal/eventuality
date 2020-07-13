from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt_claims, verify_jwt_in_request

from project.app import jwt
from project.utils.auth.exceptions import (AdminLevelRequired,
                                           UserRoleNotSufficed)


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
        claims['roles'] = [{r.promoter: r.role} for r in promoter_user_role]

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


def requires_access_level(required_role: int):
    def decorator(fn):
        @wraps(fn)
        def decorated_function(*args, **kwargs):
            pass
            # if not session.get('email'):
            #     return redirect(url_for('users.login'))
# 
            # user = User.find_by_email(session['email'])
            # elif not user.allowed(access_level):
            #     return redirect(url_for('users.profile', message="You do not have access to that page. Sorry!"))
            # return f(*args, **kwargs)
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
