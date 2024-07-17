#!/usr/bin/env python3
""" The flask app module
"""
from auth import Auth
from flask import Flask, jsonify, request


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
