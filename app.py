import uuid
import os

from flask import Flask
from flask import render_template, request, redirect, make_response, url_for
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.middleware.shared_data import SharedDataMiddleware
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from database import db_session, init_db
from login import login_manager
from models import User, Topic, Post

app = Flask(__name__)

app.secret_key = "ssucuuh398nuwetubr33rcuhne"

login_manager.init_app(app)
init_db()


@app.route('/')
def main():
    topics = Topic.query.all()
    return render_template("main.html", topics=topics)



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
    else:
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        user = User(username=username, password=password)
        db_session.add(user)
        db_session.commit()
        return redirect(url_for('login'))


@app.route('/newtopic', methods=['GET', 'POST'])
def new_topic():
    if request.method == 'GET':
        return render_template('new_topic.html')

    elif request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        topic = Topic(name=name, description=description)
        db_session.add(topic)
        db_session.commit()
        return redirect(url_for('main'))


@app.route('/posts/<topic_id>')
def list_posts(topic_id):
    return render_template('posts.html', posts=Post.query.filter_by(topic_id=topic_id).all())


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.filter_by(id=post_id).first()

    return render_template('post.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if request.method == 'GET':
        return render_template('edit_post.html', post=post)
    elif request.method == 'POST':
        post.name = request.form['name']
        post.author = request.form['author']
        post.content = request.form['content']
        db_session.commit()

        return redirect(url_for('show_post', post_id=post.post_id))


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    db_session.delete(post)
    db_session.commit()

    return redirect(url_for('list_posts'))


@app.route('/posts/<topic_id>/new', methods=['GET', 'POST'])
@login_required
def new_post(topic_id):
    if request.method == 'GET':
        return render_template('new_post.html')

    elif request.method == 'POST':
        author = request.form['author']
        name = request.form['name']
        content = request.form['content']
        post = Post(name=name, author=author, content=content, topic_id=topic_id)
        db_session.add(post)
        db_session.commit()
        return redirect(url_for('list_posts'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    response = None
    if request.method == 'GET':
        response = make_response(render_template('login.html'))
    else:
        response = make_response(redirect(url_for('main')))

        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            user.login_id = str(uuid.uuid4())
            db_session.commit()
            login_user(user)
    return response


if __name__ == '__main__':
    app.run()
