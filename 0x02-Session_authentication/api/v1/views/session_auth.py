#!/usr/bin/env python3
"""session authentication views"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User
import os


@app_views.route(
        '/auth_session/login',
        methods=['POST'],
        strict_slashes=False
        )
def login():
    """ The login view
    """
    from api.v1.app import auth
    email = request.form.get('email')
    if not email:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if not password:
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({"email": email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    session_id = auth.create_session(user.id)
    session_name = os.getenv("SESSION_NAME", "_my_session_id")
    resp = jsonify(user.to_json())
    resp.set_cookie(session_name, session_id)
    return resp


@app_views.route(
        '/auth_session/logout',
        methods=['DELETE'],
        strict_slashes=False
        )
def logout():
    """ The logout view
    """
    from api.v1.app import auth
    destroy = auth.destroy_session(request)
    if destroy is False:
        abort(404)
    return jsonify({}), 200
