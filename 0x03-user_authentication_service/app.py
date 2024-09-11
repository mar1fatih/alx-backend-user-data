#!/usr/bin/env python3
""" Flask app """
from flask import Flask, jsonify, request, abort, make_response, redirect
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
            return redirect('/')
        else:
            abort(403)
    else:
        abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """ respond with a 200 HTTP status if  the user exist"""
    session_id = request.cookies.get('session_id')
    usr = AUTH.get_user_from_session_id(session_id)
    if session_id and usr:
        return jsonify({"email": "{}".format(usr.email)}), 200
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """reset password"""
    email = request.form.get('email')
    try:
        token = AUTH.get_reset_password_token(email)
        data = {"email": "{}".format(email),
                "reset_token": "{}".format(token)}
        return jsonify(data), 200
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """update user's password"""
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)
    else:
        return jsonify({"email": email, "message": "Password updated"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port="5000")
