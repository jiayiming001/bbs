from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    make_response,
)

main = Blueprint('topic', __name__)

from .index import current_user
from models.topic import Topic
from models.board import Board
import uuid

csrf_tokens = dict()

@main.route("/")
def index():
    board_id = int(request.args.get("board_id", -1))
    if board_id == -1:
        ms = Topic.all()
    else:
        ms = Topic.find_all(board_id=board_id)
    token = str(uuid.uuid4())
    u = current_user()
    csrf_tokens['token'] = u.id
    all_board = Board.all()
    return render_template("topic/index.html", ms=ms,all_board=all_board, token=token)

@main.route("/<int:id>")
def detail(id):
    m = Topic.get_views(id)
    return render_template("/topic/detail.html", topic=m)


@main.route("/new")
def new():
    u = current_user()
    if u is None:
        return redirect(url_for('index.index'))
    else:
        bs = Board.all()
        return render_template("topic/new.html", bs=bs)


@main.route("/add", methods=["POST"])
def add():
    u = current_user()
    if u is None:
        return redirect(url_for("index.index"))
    else:
        form = request.form
        t = Topic.new(form, user_id=u.id)
        return redirect(url_for(".detail", id=t.id))



