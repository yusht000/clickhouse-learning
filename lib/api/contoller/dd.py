# coding: utf-8

from flask import Blueprint, jsonify, request

from interceptor.basic_auth import requires_auth


dd_bp = Blueprint(
    'dd',
    __name__
)

@dd_bp.route("test/jj/col.gif", methods=['POST'])
@requires_auth
def function_api_probe_post():

    '''

    :return:
    '''
    if (request.is_json is False and "event" not in request.args) or (request.is_json is True  and "event" not in request.json):

        return jsonify(
            {
                "status" : "error"
            }, 400
        )

    else:

        return jsonify(
            {
                "status" : "ok"
            }
        ), 200





