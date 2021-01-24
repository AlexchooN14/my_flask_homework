from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URL'] = 'sqllite:////tmp/test.db'
db = SQLAlchemy(app)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(30), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r' % self.username


@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        User(username=username, password=password)
    return render_template("register.html")


@app.route('/')
def hello_world():
    return 'Hello World!'


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


if __name__ == '__main__':
    app.run()
