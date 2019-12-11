import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'whatever'

    # export MAIL_SERVER='localhost'; export MAIL_PORT=8025
    # python -m smtpd -n -c DebuggingServer localhost:8025
    # pybabel extract -F babel.cfg -k _l -o messages.pot .

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['admin@microblog.lol']

    POSTS_PER_PAGE = 10
    LANGUAGES = ['en', 'sr']

    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
