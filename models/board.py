from models.pymongodb import Mongodb

"""
class Board(Model):

    def __init__(self, form):
        self.id = None
        self.title = form.get('title', '')
        self.ct = int(time.time())
        self.ut = self.ct

"""

class Board(Mongodb):
    __fields__  = Mongodb.__fields__ + [
        ('title', str, ''),
    ]


if __name__ == "__main__":
    Board.new({'title': '电子竞技'})
    Board.new({'title': '旅行拍照'})
    Board.new({'title': '学习生活'})