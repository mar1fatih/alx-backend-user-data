#!/usr/bin/env python3
""" Flask app """
from flask import Flask, jsonify, request, abort, make_response
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


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """create new session for the user, store it the session ID as a cookie"""
    email = request.form.get('email')
    password = request.form.get('password')
    if email and password and AUTH.valid_login(email, password):
        _id = AUTH.create_session(email)
        data = {"email": "{}".format(email), "message": "logged in"}
        resp = make_response(jsonify(data), 200)
        resp.set_cookie('session_id', _id)
        return resp
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """destroy the session and redirect the user to GET /"""
    session_id = request.cookies.get('session_id')
    if session_id:
        usr = AUTH.get_user_from_session_id(session_id)
        if usr:
            AUTH.destroy_session(usr.id)
            resp = make_response(redirect('/'))
            return resp
        else:
            abort(403)
    else:
        abort(403)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port="5000")
