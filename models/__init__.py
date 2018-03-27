'''
import json
import os

def save(data, path):
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        f.write(s)

     # with open(path, 'w+', encoding='utf-8') as f:
     #       json.load(data, f)


def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = f.read()
        return json.loads(data)

    # with open(path, 'r', encoding='utf-8') as f:
    #   return json.load(data, f)


class Model(object):

    @classmethod
    def db_path(cls):
        classname = cls.__name__
        path = os.path.dirname(os.path.dirname(__file__))
        path += '/data/{}.txt'.format(classname)
        path = os.path.abspath(path)
        return path

    @classmethod
    def _new_from_dict(cls, data):
        m = cls({})
        for k, v in data.items():
            setattr(m, k, v)
        return m

    @classmethod
    def new(cls, form, **kwargs):
        m = cls(form)
        for k, v in kwargs.items():
            setattr(m, k, v)
        m.save()
        return m

    @classmethod
    def all(cls):
        models = load(cls.db_path())
        s = [cls._new_from_dict(m) for m in models]
        return s

    @classmethod
    def find_all(cls, **kwargs):
        ms = []
        models = cls.all()
        for i in models:
            for k, v in kwargs.items():
                if hasattr(i, k) and getattr(i, k) == v:
                    ms.append(i)
        return ms


    @classmethod
    def find_by(cls, **kwargs):
        models = cls.all()
        for m in models:
            for k, v in kwargs.items():
                if  hasattr(m, k) and getattr(m, k) == v:
                    return m
        return None

    @classmethod
    def find(cls, id):
        return cls.find_by(id = id)

    @classmethod
    def delete(cls, id):
        models = cls.all()
        index = -1
        for i, m in enumerate(models):
            if m.id == id:
                index = i
                break
        if index == -1:
            pass
        else:
            obj = models.pop(index)
            l = [m.__dict__ for m in models]
            path = cls.db_path()
            save(l, path)
            return obj


    def save(self):
        path = self.db_path()
        models = self.all()
        if self.id == None:
            if  len(models) == 0:
                self.id = 1
            else:
                m = models[-1]
                self.id = m.id + 1
            models.append(self)
        else:
            for i, m in enumerate(models):
                if m.id == self.id:
                    models[i] = self
                    break
        data = [m.__dict__ for m in models]
        save(data, path)


    def __repr__(self):
        """
        __repr__ 是一个魔法方法
        简单来说, 它的作用是得到类的 字符串表达 形式
        比如 print(u) 实际上是 print(u.__repr__())
        """
        classname = self.__class__.__name__
        properties = ['{}: {}'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '<{}\n{}\n>\n'.format(classname, s)


    def json(self):
        d = self.__dict__.copy()
        return d

'''