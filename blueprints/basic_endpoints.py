import os

from flask import abort, Blueprint, request
from redis import Redis
from flask import jsonify

blueprint = Blueprint('api', __name__, url_prefix='/v1')
redis = Redis(host=os.environ.get("REDIS_HOST", '127.0.0.1'), port=6379)

@blueprint.route('/variables', methods=['GET'])
def get_variables():
    return {key.decode('utf-8'): redis.get(key).decode('utf-8')
                                    for key in redis.scan_iter()}


@blueprint.route('/variables/<key>', methods=['GET'])
def get_variable(key):
    value = redis.get(key)

    if value is None:
        abort(404)
    else:
        return {key: value.decode('utf-8')}


@blueprint.route('/variables/', methods=['POST'])
def set_variable():
    if not request.json or not 'key' in request.json or not 'value' in request.json:
        abort(400)

    if redis.get(request.json.get('key')) is not None:
        return jsonify({'error': 'Variable exists!'}), 400

    key = request.json.get('key')
    value = request.json.get('value')

    redis.set(name=key, value=value)
    return jsonify({key: value}), 201


@blueprint.route('/variables/<key>', methods=['PUT'])
def update_variable(key):
    if not request.json or not 'value' in request.json:
        abort(400)

    if redis.get(key) is None:
        return jsonify({'error': 'Variable not found!'}), 404

    value = request.json.get('value')

    redis.set(name=key, value=value)
    return jsonify({key: value}), 200
