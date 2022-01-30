# coding: utf-8

from functools import wraps
from flask  import  request, Response
from config.setting import BASIC_AUTH

def check_auth(username, password):

    return username == BASIC_AUTH.get('USER')  and password == BASIC_AUTH.get('PASSWORD')

def authenticate():

    return Response(
        u'Could not verify your access level for that url.<br/>'
        u'You have to login with username and password for api administrator.<br/>'
        u'2020.<br/>'
        u'<br/>by ', 401,
        {
            'WWW-Authenticate': 'Basic realm="Login Required"'
        }
    )


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password) :
            return authenticate()
        return f(*args, **kwargs)
    return  decorated()






