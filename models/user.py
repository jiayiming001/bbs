from .pymongodb import Mongodb


"""
class User(Model):

    def __init__(self, form):
        self.id = form.get('id', None)
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.user_image = 'default.png'


    def salt_password(self, password, salt="@#$@#%^5SAD"):
        import  hashlib
        def sha256(ascii_str):
            return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()
        hash1 = sha256(password)
        hash2 = sha256(hash1 + salt)
        return hash2

    '''
    def hashed_password(self, pwd):
        import hashlib
        p = pwd.encode('ascii')
        s = hashlib.sha256(p)
        return s
    '''

    @classmethod
    def register(cls, form):
        name = form.get('username', '')
        pwd = form.get('password', '')
        if len(name) > 2 and User.find_by(username=name) is None:
            u =  User.new(form)
            u.password = u.salt_password(pwd)
            u.username = name
            u.save()
            return u
        else:
            return None

    @classmethod
    def validate_login(cls, form):
        name = form.get('username', '')
        pwd = form.get('password', '')
        u = User.find_by(username=name)
        print(u)
        u2 = User(form)
        if u is not None and u2.salt_password(pwd) == u.password:
            return u
        else:
            return None
"""

class User(Mongodb):
    __fields__ = Mongodb.__fields__ + [
        ('username', str, ''),
        ('password', str, ''),
        ('user_image', str, 'default.gif'),
    ]

    def __init__(self):
        self.user_image = 'default.gif'


    def salt_password (self, password, salt="@#$@#%^5SAD"):
        import hashlib
        def sha256 (ascii_str):
            return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()

        hash1 = sha256(password)
        hash2 = sha256(hash1 + salt)
        return hash2


    @classmethod
    def register (cls, form):
        name = form.get('username', '')
        pwd = form.get('password', '')
        if len(name) > 2 and User.find_by(username=name) is None:
            u = User.new(form)
            u.password = u.salt_password(pwd)
            u.username = name
            u.save()
            return u
        else:
            return None

    @classmethod
    def validate_login (cls, form):
        name = form.get('username', '')
        pwd = form.get('password', '')
        u = User.find_by(username=name)
        u2 = User()
        if u is not None and u2.salt_password(pwd) == u.password:
            return u
        else:
            return None