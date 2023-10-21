import os

from flask import abort, Blueprint, request
from redis import Redis


blueprint = Blueprint('api', __name__, url_prefix='/v1')
redis = Redis(host=os.environ.get("REDIS_HOST", '127.0.0.1'), port=6379)

@blueprint.route('/', methods=['GET', 'POST', 'PUT'])
def endpoint():
    if request.method == "GET":
        # get(key)
        key = request.args.get('key')
        if key is not None:
            value = redis.get(key)

            if value is None:
                abort(404, "Key is not defined!")
            else:
                return {key: value.decode('utf-8')}
        else:
            # all()
            return {key.decode('utf-8'): redis.get(key).decode('utf-8')
                      for key in redis.scan_iter()}

    elif request.method == "POST":
        excepted = []
        for key, value in request.args.items():
            if redis.get(key) is None:
                redis.set(name=key, value=value)
            else:
                excepted.append(key)
        if len(excepted) > 0:
            inline_excepted = ', '.join(excepted)
            abort(412, f"Variables exists!\n\
                        Variables: {inline_excepted} - exists in DB!")
        else:
            return {'status': 'Ok'}

    elif request.method == "PUT":
        exists = redis.exists(*list(request.args.keys()))

        if exists == len(request.args.keys()):
            for key, value in request.args.items():
                redis.set(name=key, value=value)
            return {'status': 'Ok'}
        else:
            abort(404, f"Variable not Found!\n")

    else:
        abort(405, "Method not allowed!")
