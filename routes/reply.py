from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    make_response,
    send_from_directory
)

main = Blueprint('reply', __name__)

from models.reply import Reply
from .index import current_user


@main.route('/add', methods=["POST"])
def add():
    form = request.form
    reply = Reply.new(form)
    u = current_user()
    reply.set_user_id(u.id)
    return redirect(url_for('topic.detail', id=reply.topic_id))