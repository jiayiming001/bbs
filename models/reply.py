from .pymongodb import Mongodb
import time

'''
class Reply(Model):

    def __init__(self, form):
        self.id = None
        self.content = form.get('content', '')
        self.ct = int(time.time())
        self.ut = self.ct
        self.topic_id = int(form.get('topic_id', -1))
        self.user_id = int(form.get('user_id', -1))


    def user(self):
        from .user import User
        u = User.find(self.user_id)
        return u

    def set_user_id(self, user_id):
        self.user_id = user_id
        self.save()

    def push_time(self):
        format = "%Y/%m/%d  %H:%M:%S"
        return time.strftime(format,time.localtime(self.ct))
'''

class Reply(Mongodb):

    __fields__  = Mongodb.__fields__+ [
        ('content', str, ''),
        ('topic_id', int, -1),
        ('user_id', int, -1),
        ('receiver_id', int, -1)
    ]


    def push_time (self):
        format = "%Y/%m/%d  %H:%M:%S"
        return time.strftime(format, time.localtime(self.ut))

    def set_user_id(self, user_id):
        self.user_id = user_id
        self.save()


    def user(self):
        from .user import User
        u = User.find_by(id=self.user_id)
        return u