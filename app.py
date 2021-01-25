from flask import Flask
from flask import render_template, request, redirect, url_for
from flask_httpauth import HTTPBasicAuth
import logging

from post import Post
from user import User

app = Flask(__name__)


auth = HTTPBasicAuth()

logging.basicConfig(filename='logs', format='%(levelname)s  %(asctime)s : %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)


# @app.route('/register', methods=["POST", "GET"])
# def register():
#     if request.method == "POST":
#         username = request.form.get("username")
#         password = request.form.get("password")
#         User(username=username, password=password)
#     return render_template("register.html")


@app.route('/')
def main():
    return render_template("main.html")


@app.route('/cars')
def cars():
    return render_template("cars_main.html")


@app.route('/cars/germany')
def germany():
    return render_template("ZaGermaniq.html")


@app.route('/cars/america')
def america():
    return render_template("ZaAmerika.html")


@app.route('/cars/japan')
def japan():
    return render_template("ZaJapan.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        values = (
            None,
            request.form['username'],
            User.hash_password(request.form['password'])
        )
        User(*values).create()

        return redirect('/')


@auth.verify_password
def verify_password(username, password):
    user = User.find_by_username(username)
    if user:
        return user.verify_password(password)

    return False


if __name__ == '__main__':
    app.run()
