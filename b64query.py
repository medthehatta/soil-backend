import json
from base64 import b64decode, b64encode
from functools import wraps


class Base64QueryManager:

    def __init__(self, app):
        self.app = app

    def decode(self, b64query_):
        return from_b64query(b64query_)

    def link(self, endpoint, query):
        b64 = to_b64query(query)
        return self.app.url_path_for(endpoint, query=b64)

    def register(self, func):

        @wraps(func)
        def _func(query):
            q = self.decode(query)
            return func(q)

        def _link(query):
            return self.link(func.__name__, query)

        setattr(self, func.__name__, _link)
        return _func


def to_b64query(query):
    return b64encode(json.dumps(query).encode("utf-8")).decode("utf-8")


def from_b64query(query):
    return json.loads(b64decode(query.encode("utf-8")).decode("utf-8"))
