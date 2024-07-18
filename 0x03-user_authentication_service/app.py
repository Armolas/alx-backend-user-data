#!/usr/bin/env python3
""" The flask app module
"""
from auth import Auth
from flask import Flask, jsonify, request, abort, redirect, url_for


app = Flask(__name__)
AUTH = Auth()


@app.route('/')
def root():
    """ root endpoint
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """ registers a new user
    """
    req = request.form
    email = req.get("email")
    password = req.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify(
                {"email": f"{email}", "message": "user created"}
                )
    except Exception:
        return jsonify(
                {"message": "email already registered"}
                ), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """ Logs a user in
    """
    req = request.form
    email = req.get("email")
    password = req.get("password")
    if AUTH.valid_login(email, password) is True:
        session_id = AUTH.create_session(email)
        resp = jsonify({"email": f"{email}", "message": "logged in"})
        resp.set_cookie("session_id", session_id)
        return resp
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """ Logs a user out
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is not None:
        AUTH.destroy_session(user.id)
        return redirect(url_for('login'))
    else:
        abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """ Gets a user profile
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is not None:
        return jsonify({"email": f"{user.email}"}), 200
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email)
        if reset_token:
            return jsonify(
                    {"email": f"{email}", "reset_token": f"{reset_token}"}
                    ), 200
        else:
            abort(403)
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
