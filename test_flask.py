# test_flask.py
from unittest import TestCase

from app import app
from models import db, User, Post

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add sample user."""

        User.query.delete()

        user = User(first_name="John", last_name="Doe", image_url="https://static.wikia.nocookie.net/john-doe-game/images/b/b2/Doe1_plus.png/revision/latest?cb=20220327075824")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user=user

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('John Doe', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('John Doe', html)
            self.assertIn(self.user.last_name, html)

    def test_add_user(self):
        with app.test_client() as client:
            d = {"first_name": "Donald", "last_name": "Trump", "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Donald_Trump_official_portrait.jpg/1024px-Donald_Trump_official_portrait.jpg"}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Donald Trump", html)


class PostViewsTestCase(TestCase):
    """Tests for views for Posts."""
    def setUp(self):
        """Add sample post."""
        Post.query.delete()
        User.query.delete()


        user = User(first_name="John", last_name="Doe", image_url="https://static.wikia.nocookie.net/john-doe-game/images/b/b2/Doe1_plus.png/revision/latest?cb=20220327075824")
        db.session.add(user)
        db.session.commit()

        post = Post(title="Title", content="Content", user_id=user.id)
        db.session.add(post)
        db.session.commit()

        self.user_id = user.id
        self.post_id = post.id
        self.user=user
        self.post=post

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_posts(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)
            print(html)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Title', html)
            self.assertIn(self.post.title, html)

    def test_show_post(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Title', html)
            self.assertIn(self.post.content, html)

    def test_add_post(self):
        with app.test_client() as client:
            d = {"title": "Breaking news!", "content": "Sponge Bob is not real!"}
            resp = client.post(f"/users/{self.user_id}/posts/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Breaking news!", html)
