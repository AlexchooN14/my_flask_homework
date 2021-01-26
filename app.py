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


@app.route('/posts')
def list_posts():
    return render_template('posts.html', posts=Post.all())


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.find(post_id)

    return render_template('post.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    post = Post.find(post_id)
    if request.method == 'GET':
        return render_template('edit_post.html', post=post)
    elif request.method == 'POST':
        post.name = request.form['name']
        post.author = request.form['author']
        post.content = request.form['content']
        post.save()

        return redirect(url_for('show_post', post_id=post.post_id))


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.find(post_id)
    post.delete()

    return redirect(url_for('list_posts'))


@app.route('/posts/new', methods=['GET', 'POST'])
@auth.login_required
def new_post():
    if request.method == 'GET':
        return render_template('new_post.html')

    elif request.method == 'POST':
        logging.info("stignahme do post")
        values = (None, request.form['name'], request.form['author'], request.form['content'])
        Post(*values).create()
        return redirect(url_for('list_posts'))


@auth.verify_password
def verify_password(username, password):
    user = User.find_by_username(username)
    if user:
        return user.verify_password(password)

    return False


if __name__ == '__main__':
    app.run()
