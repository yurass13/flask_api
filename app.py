import os

from flask import abort, Flask, json, request
from redis import Redis


app = Flask(__name__)
redis = Redis(host=os.environ.get("REDIS_HOST", '127.0.0.1'), port=6379)

@app.route('/', methods=['GET', 'POST', 'PUT'])
def endpoint():
    if request.method == "GET":
        # get(key)
        key = request.args.get('key')
        if key is not None:
            value = redis.get(key)

            if value is None:
                abort(404, "Key is not defined!")
            else:
                return json.dumps({key: value.decode('utf-8')})
        else:
            # all()
            data = {key.decode('utf-8'): redis.get(key).decode('utf-8')
                                         for key in redis.scan_iter()}
            return json.dumps(data)

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
            return ""

    elif request.method == "PUT":
        exists = redis.exists(*list(request.args.keys()))

        if exists == len(request.args.keys()):
            for key, value in request.args.items():
                redis.set(name=key, value=value)
            return ""
        else:
            abort(404, f"Variable not Found!\n")
    else:
        abort(405, "Method not allowed!")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port='8080', debug=True)