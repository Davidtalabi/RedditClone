class Config(object):
    DEBUG = False
    TESTING = False

    db_username = 'b263a92eebff95'
    db_password = 'd872a629'
    db_host = 'us-cdbr-east-03.cleardb.com'
    db_db = 'heroku_634870331b65831'

    SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@{}/{}'.format(db_username,
                                                           db_password,
                                                           db_host,
                                                           db_db)

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True