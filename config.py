class Config(object):
    DEBUG = False
    TESTING = False

    #ive hidden my uri for security purposes
    db_username = '#'
    db_password = '#'
    db_host = '#'
    db_db = '#'

    SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@{}/{}'.format(db_username,
                                                           db_password,
                                                           db_host,
                                                           db_db)

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
