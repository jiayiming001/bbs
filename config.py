import os

user_file_director = os.path.join(os.path.dirname(__file__), 'static','user_images')
user_file_director = os.path.abspath(user_file_director)
accept_user_file_type = ['png','jpg', 'gif']

secret_key = 'jia_bbs'


mgconfig = {
    'host':"127.0.0.1",
    'port':27017,
    'db_name':"bbsdb",
    'set_name': "User"
}


class Config(object):
    pass

class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True