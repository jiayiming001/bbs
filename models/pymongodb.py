from pymongo import MongoClient
from config import mgconfig
from time import time

try:
    mongo = MongoClient(mgconfig['host'], mgconfig['port'])
except Exception as e:
    print(e)



def  next_id(name):
    query = {
        'name':name,
    }
    update = {
        '$inc': {
            'seq': 1
        }
    }
    kwargs ={
        'query': query,
        'update': update,
        'upsert': True,
        'new': True,
    }
    doc = mongo.db['data_id']
    new_id = doc.find_and_modify(**kwargs).get('seq')
    return new_id

class Mongodb(object):

    __fields__= [
        '_id',
        ('id', int, -1),
        ('type', str, ''),
        ('ct', int, 0),
        ('ut', int , 0),
        ('deleted', bool, False)
    ]


    @classmethod
    def new(cls, form, **kwargs):
        m = cls()
        name = cls.__name__
        if form is None:
            form = {}
        fields = cls.__fields__.copy()
        for f in fields:
            k, t, v = f
            if k in form:
                setattr(m, k, t(form[k]))
            else:
                setattr(m, k ,v)

        for k, v in kwargs.items():
            if hasattr(m, k):
                setattr(m, k, v)
            else:
                raise KeyError
        ts = int(time())
        m.ct = ts
        m.ut = ts
        m.id = next_id(name)
        m.type = name.lower()
        m.save()
        return m


    @classmethod
    def  _new_with_bson(cls, bson):
        m = cls()
        fields = cls.__fields__.copy()
        fields.remove('_id')
        for f in fields:
            k, t, v = f
            if k in bson:
               setattr(m, k, bson[k])
            else:
                setattr(m, k, v)

        setattr(m, '_id', bson['_id'])
        m.type = cls.__name__.lower()
        return m


    @classmethod
    def all(cls):
        return cls._find()

    @classmethod
    def _find(cls, **kwargs):
        name = cls.__name__
        flag_sort = '__sort'
        sort = kwargs.pop(flag_sort, None)
        ds = mongo.db[name].find(kwargs)
        if sort is not None:
            ds = ds.sort(sort)
        l = [cls._new_with_bson(d) for d in ds]
        return l


    @classmethod
    def _find_raw(cls, **kwargs):
        name = cls.__name__
        ds = mongo.db[name].find(kwargs)
        l = list(ds)
        return l


    @classmethod
    def _clean_field(cls, source, target):
        ms = cls._find()
        for m in ms:
            v = getattr(m, source)
            setattr(m, target, v)
            m.save()


    def save(self):
        name = self.__class__.__name__
        mongo.db[name].save(self.__dict__)

    @classmethod
    def find_by(cls, **kwargs):
        return cls.find_one(**kwargs)


    @classmethod
    def find_all(cls, **kwargs):
       return cls._find(**kwargs)


    @classmethod
    def find(cls, id):
        return cls.find_one(id=id)

    @classmethod
    def get(cls, id):
        return cls.find_one(id=id)

    @classmethod
    def find_one(cls, **kwargs):
        l = cls._find(**kwargs)
        if len(l) > 0:
            return l[0]
        else:
            return None

    @classmethod
    def upsert(cls, query_form, update_form, hard=False):
        ms = cls.find_one(**query_form)
        if ms is None:
            query_form.update(**update_form)
            ms = cls.new(query_form)
        else:
            ms.update(update_form, hard=hard)
        return ms

    def update(self, form, hard=False):
        for k, v in form.items():
            if hard or hasattr(self, k):
                setattr(self, k, v)
        self.save()



    def delete(self):
        name = self.__class__.__name__
        query = {
            'id':self.id,
        }
        values = {
            'deleted':True,
        }
        mongo.db[name].update_one(query, values)


    def blacklist(self):
        b = [
            '_id',
        ]
        return b


    def json(self):
        _dict = self.__dict__
        d = {k:v for k, v in _dict.items() if k not in self.blacklist()}
        return d


    def data_count(self, cls):
        name = cls.__name__
        fk = '{}_id'.format(self.__class__.__name__.lower())
        query = {
            fk:self.id,
        }
        count = mongo.db[name]._find(query).count()
        return count


    def __repr__ (self):
        class_name = self.__class__.__name__
        properties = ('{0} = {1}'.format(k, v) for k, v in self.__dict__.items())
        return '<{0}: \n  {1}\n>'.format(class_name, '\n  '.join(properties))
