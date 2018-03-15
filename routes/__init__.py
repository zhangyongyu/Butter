import uuid
from functools import wraps

from flask import session, request, abort
# import redis

from models.user import User
from utils import log


def current_user():
    uid = session['user_id']
    u = User.one(id=uid)
    return u


csrf_tokens = dict()
# redis 自动转码
# r = redis.StrictRedis(charset="utf-8", decode_responses=True)


def csrf_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args.get('token')
        u = current_user()
        # if token in csrf_tokens and csrf_tokens[token] == u.id:
        log('check token', token, u.id, r.exists(token), r.get(token))
        # if r.exists(token) and r.get(token) == u.id:
        # r.delete(token)
        if token in csrf_tokens:
            uid = csrf_tokens.pop(token)
            if uid == u.id:
                return f(*args, **kwargs)
        else:
            abort(401)

    return wrapper


def new_csrf_token():
    u = current_user()
    token = str(uuid.uuid4())
    csrf_tokens[token] = u.id
    # r.set(token, u.id)
    # log('new token', token, u.id)
    return token
