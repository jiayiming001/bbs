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

import os
from werkzeug.utils import secure_filename
from models.user import User
from config import user_file_director
from utils import log

main = Blueprint('index', __name__)

def current_user():
    id = session.get('user_id', -1)
    u = User.find_by(id=id)
    return u

@main.route('/')
def index():
    return render_template('index.html')


@main.route('/login', methods=['POST'])
def login():
    form = request.form
    u = User.validate_login(form)
    if u is None:
        return redirect(url_for('.index'))
    else:
        print(u)
        session['user_id'] = u.id
        session.permanent = True
        return redirect(url_for('.profile'))

@main.route('/register', methods=['POST'])
def register():
    form = request.form
    u = User.register(form)
    return redirect(url_for('.index'))

@main.route('/profile')
def profile():
    u = current_user()
    if u is None:
        return redirect(url_for('.index'))
    else:
        return render_template('profile.html', user=u)


def allow_file(filename):
    suffix = filename.split(".")[-1]
    from config import accept_user_file_type
    return suffix in accept_user_file_type


@main.route('/add_img', methods=["POST"])
def add_img():
    u = current_user()
    if u is None:
        return redirect(url_for('.index'))

    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    if allow_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(user_file_director, filename))
        u.user_image = filename
        u.save()
    return redirect(url_for(".profile"))


@main.route("/uploads/<filename>")
def uploads(filename):
    return send_from_directory(user_file_director, filename)