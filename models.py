# models.py
"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


# MODELS GO BELOW!
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    image_url = db.Column(db.String)

    def __repr__(self):
        return f'<User id={self.id}, first_name "{self.first_name}", last_name "{self.last_name}", image_url "{self.image_url}">'

    def greet(self):
        return f'Hi, I am {self.first_name} {self.last_name}'
 
class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'))

    users=db.relationship('User', backref='posts')

    tagging=db.relationship('PostTag', backref='post')

    tags=db.relationship('Tag', secondary='posts_tags', backref='posts')

    def __repr__(self):
        return f'<Post id={self.id}, title "{self.title}", content "{self.content}", created_at {self.created_at}>'
    
    def description(self):
        return f'The title is {self.title}, the content is {self.content}'
    
class Tag(db.Model):
    __tablename__='tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    posts = db.relationship('Post', secondary='posts_tags', backref='tags')

    tagging=db.relationship('PostTag', backref='tag')

class PostTag(db.Model):
    __tablename__='posts_tags'

    post_id=db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id=db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

    def __init__(self, post_id, tag_id):
        self.post_id=post_id
        self.tag_id=tag_id

def get_directory():
    all_posts=Post.query.all()

    for p in all_posts:
        print(p.users.first_name, p.users.last_name, p.title, p.content)

def get_directory_join():
    directory=db.session.query(Post.title, User.first_name, User.last_name).join(User).all()

    for title, first_name, last_name in directory:
        print (first_name, last_name, title)

def get_directory_join_class():
    directory=db.session.query(Post, User).join(User).all()
    
    for post, user in directory:
        print (user.first_name, user.last_name, post.title)

def get_directory_all_join():
    directory=db.session.query(Post.title, User.first_name, User.last_name).outerjoin(User).all()

    for title, first_name, last_name in directory:
        print (first_name, last_name, title)