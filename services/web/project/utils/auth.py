from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_claims
from project.app import jwt
# from project.apps.promoter.models.promoterUserRole import PromoterUserRole
# 
# 
# @jwt.user_claims_loader
# def add_claims_to_access_token(identity):
#     roles = PromoterUserRole.query.filter_by(user_id=identity)
#     roles = [role.role for role in roles]
#     return {
#         'roles': roles
#     }



def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        print(claims)
        # if claims['roles'] != 'admin':
        #     return jsonify(msg='Admins only!'), 403
        # else:
        #     return fn(*args, **kwargs)
    return wrapper


def role_required(fn, role):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['roles'] != 'admin':
            return jsonify(msg='Admins only!'), 403
        else:
            return fn(*args, **kwargs)
    return wrapper