from .user import User
from .pymongodb import Mongodb
import json


"""
class Topic(Model):


    def __init__(self, form):
        self.id = None
        self.views = 0
        self.title = form.get('title', '')
        self.content = form.get('content', '')
        self.ct = int(time.time())
        self.ut = self.ct
        self.user_id = form.get('user_id', '')
        self.board_id = int(form.get('board_id', -1))


    @classmethod
    def get_views(cls, id):
        m = cls.find_by(id=id)
        m.views += 1
        m.save()
        return m

    def replies(self):
        from .reply import Reply
        rs = Reply.find_all(topic_id = self.id)
        return rs

    def user(self):
        u = User.find_by(id=self.user_id)
        return u
"""
class Cache(object):
    def get(self, key):
        pass

    def set(self, key, value):
        pass

class RedisCache(Cache):
    import redis
    redis_db = redis.StrictRedis(host='localhost', port=6379, db=0)

    def set(self, key, value):
        return self.__class__.redis_db.set(key, value)

    def get(self, key):
        return self.__class__.redis_db.get(key)


class Topic(Mongodb):
    __fields__ = Mongodb.__fields__ + [
        ('content', str, ''),
        ('title', str, ''),
        ('user_id', int, -1),
        ('board_id', int, -1),
        ('views', int, 0),
    ]

    should_update_all = True
    redis_cache = RedisCache()
    def to_json(self):
        d = dict()
        for k in Topic.__fields__:
            key = k[0]
            if not key.startswith('_'):
                d[key] = getattr(self, key)
        return json.dumps(d)

    @classmethod
    def from_json(cls, j):
        d = json.loads(j)
        instance = cls()
        for k, v in d.items():
            setattr(instance, k, v)
        return instance

    @classmethod
    def all_delay(cls):
        return Topic.all()

    @classmethod
    def get(cls, id):
        m = cls.find_by(id=id)
        m.views += 1
        m.save()
        return m

    def save(self):
        super(Topic, self).save()
        self.__class__.should_update_all = True

    @classmethod
    def cache_all(cls):
        if cls.should_update_all:
            cls.redis_cache.set('topic_all', json.dumps([i.to_json() for i in cls.all_delay()]))
            cls.should_update_all = False
        j = json.loads(cls.redis_cache.get('topic_all').decode('utf-8'))
        j = [cls.from_json(i) for i in j]
        return j


    def replies(self):
        from .reply import Reply
        ms = Reply.find_all(topic_id=self.id)
        return ms

    def board(self):
        from .board import Board
        m = Board.find(self.board_id)
        return m


    def user(self):
        u = User.find(id=self.user_id)
        return u

    @classmethod
    def get_views(cls, id):
        m = cls.find_one(id=id)
        m.views += 1
        m.save()
        return m
