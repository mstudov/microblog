from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.models import User, Post
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

class UserModelCase(unittest.TestCase):
    # executes before each test
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    # executes after each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_avatar(self):
        u = User(username='mirko', email='mirko@whatever.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                        '2f2ea3a5773faa9cae3d0ccd47eef2c1'
                                        '?d=retro&s=128'))

    def test_follow(self):
        u1 = User(username='mirko', email='mirko@whatever.com')
        u2 = User(username='jovan', email='jovan@whatever.com')

        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u2.followed.all(), [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, 'jovan')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, 'mirko')

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    def test_follow_posts(self):
        u1 = User(username='mirko', email='mirko@whatever.com')
        u2 = User(username='jovan', email='jovan@whatever.com')
        u3 = User(username='milan', email='milan@whatever.com')
        u4 = User(username='petar', email='petar@whatever.com')
        db.session.add_all([u1, u2, u3, u4])

        now = datetime.utcnow()
        p1 = Post(body="post from mirko", author=u1,
                  timestamp=now + timedelta(seconds=1))
        p2 = Post(body="post from jovan", author=u2,
                  timestamp=now + timedelta(seconds=4))
        p3 = Post(body="post from milan", author=u3,
                  timestamp=now + timedelta(seconds=3))
        p4 = Post(body="post from petar", author=u4,
                  timestamp=now + timedelta(seconds=2))
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        u1.follow(u2) # mirko follows jovan
        u1.follow(u4) # mirko follows petar
        u2.follow(u3) # jovan follows milan
        u3.follow(u4) # milan follows petar
        db.session.commit()

        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()
        self.assertEqual(f1, [p2, p4, p1])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])

if __name__ == '__main__':
    unittest.main(verbosity=2)
