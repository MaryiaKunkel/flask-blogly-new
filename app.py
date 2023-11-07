# app.py
"""Blogly application."""

from flask import Flask, request, render_template, redirect
from models import User, Post, Tag, PostTag, db, connect_db, get_directory, get_directory_join, get_directory_join_class, get_directory_all_join

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "chickenzarecool21837"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

connect_db(app)

app.app_context().push()


@app.route('/')
def redirect_to_users():
    return redirect('/users')

@app.route('/users')
def user_listing_page():
    '''User listing''' 
    users=User.query.all()
    return render_template('user_listing.html', users=users)

@app.route('/users/new')
def new_user_page():
    '''Page with input fields for a new user'''
    return render_template('new_user.html')


@app.route('/users/new', methods=['POST'])
def save_user_page():
    '''Saving the info from the inputs to the db'''
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    image_url = request.form.get('image_url')

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def user_detail_page(user_id):
    '''Page with the user details'''
    user=User.query.get_or_404(user_id)
    posts=user.posts
    return render_template('user_details.html', user=user, posts=posts)


@app.route('/users/<int:user_id>/edit')
def user_edit_page(user_id):
    '''Page to edit user details'''
    user=User.query.get_or_404(user_id)
    return render_template('user_edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def save_edited_user(user_id):
    '''Save edited user details'''
    user=User.query.get_or_404(user_id)
    user.first_name = request.form.get('first_name')
    user.last_name = request.form.get('last_name')
    user.image_url = request.form.get('image_url')

    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    '''Delete user'''
    user=User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/posts/new')
def new_post(user_id):
    '''Show form to add a post for that user'''
    user=User.query.get(user_id)
    return render_template('new_post.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_new_post(user_id):    
    '''Add post and redirect to the user detail page'''
    title = request.form.get('title')
    content = request.form.get('content')

    new_post = Post(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def post_detail_page(post_id):
    '''Show a post'''
    post=Post.query.get_or_404(post_id)
    user=User.query.get_or_404(post.user_id)
    return render_template('post_detail.html', post=post, user=user)

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    '''Show form to edit a post'''
    post=Post.query.get_or_404(post_id)
    return render_template('post_edit.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def save_edited_post(post_id):
    '''Save edited post details'''
    post=Post.query.get_or_404(post_id)    
    post.title = request.form.get('title')
    post.content = request.form.get('content')

    db.session.commit()

    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    '''Delete post'''
    post=Post.query.get_or_404(post_id)
    user=User.query.get_or_404(post.user_id)
    user_id=user.id
    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')