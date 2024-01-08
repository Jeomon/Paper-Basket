from os import path
root_path=path.abspath(".")
temp_folder=path.join(root_path,'temp')

class Config(object):
    TEMPLATES_AUTO_RELOAD=True
    MAIL_SERVER='localhost'
    MAIL_PORT=1025
    MAIL_USERNAME='no-reply@paperbasket.com'
    MAIL_PASSWORD='123'
    MAIL_DEFAULT_SENDER='no-reply@paperbasket.com'
    MAIL_MAX_EMAILS=None
    MAIL_ASCII_ATTACHMENTS=False
    SESSION_COOKIE_ENABLED= False
    CACHE_TYPE='RedisCache'
    CACHE_DEFAULT_TIMEOUT=300
    CACHE_REDIS_HOST='localhost'
    CACHE_REDIS_PORT=6379
    CACHE_REDIS_DB='3'
    SECRET_KEY="b9476566e7f09d64b136ad1a"
    SECURITY_PASSWORD_SALT="1ad7f045d76225ff660c57999e675dc9"
    SECURITY_PASSWORD_HASH="bcrypt"
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SECURITY_TOKEN_AUTHENTICATION_HEADER="Authentication-Token"
    SQLALCHEMY_DATABASE_URI="sqlite:///" + path.join(root_path,'database','account.sqlite3')
    SQLALCHEMY_BINDS={"product":"sqlite:///" + path.join(root_path,'database','product.sqlite3'),
                      "order":"sqlite:///" + path.join(root_path,'database','order.sqlite3')}