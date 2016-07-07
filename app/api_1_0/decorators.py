from functools import wraps
from .errors import forbidden
from flask import g

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.current_user.is_administrator:
            return forbidden('Administrator Only')
        return f(*args, **kwargs)
    return decorated_function
