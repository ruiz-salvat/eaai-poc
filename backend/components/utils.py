from flask import session
from components.models import User


def current_user():
    if 'id' in session:
        uid = session['id']
        print(f'\session id:\n{str(uid)}\n', flush=True)
        return User.query.get(uid)
    return None


def split_by_crlf(s):
    return [v for v in s.splitlines() if v]