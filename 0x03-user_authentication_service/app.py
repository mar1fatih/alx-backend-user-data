#!/usr/bin/env python3
""" Flask app """
from flask import Flask, jsonify, request
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def bienvenue():
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def addUser():
    """end point to add a user"""
    email = request.form.get('email')
    pss = request.form.get('password')
    try:
        AUTH.register_user(email, pss)
        res = {"email": "{}".format(email), "message": "user created"}
        return jsonify(res), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port="5000")
