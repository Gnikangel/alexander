import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLE = True
    SQL_DB = 'hola'


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
