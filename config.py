import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLE = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    DB_URI = (
        "postgresql+psycopg2://{username}:{password}@{hostname}/"
        "{databasename}".format(
            username="postgres", password="postgres",
            hostname="localhost", databasename="prometheus"))
    SQLALCHEMY_DATABASE_URI = DB_URI


class ProductionConfig(Config):
    DEBUG = False


class StagingConf(Config):
    DEVELOMENT = True
    DEBUG = True


class DevelomentConfig(Config):
    DEVELOMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
