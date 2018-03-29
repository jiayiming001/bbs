from flask import Flask
from config import secret_key, DevConfig


app = Flask(__name__)
app.config.from_object(DevConfig)
app.secret_key = secret_key

from routes.index import main as index_routes
app.register_blueprint(index_routes)
from routes.topic import main as topic_routes
app.register_blueprint(topic_routes, url_prefix="/topic")
from routes.reply import main as reply_routes
app.register_blueprint(reply_routes, url_prefix="/reply")


if __name__ == '__main__':

    config = dict(
        debug=True,
        host='0.0.0.0',
        port=2001,
    )
    app.run(**config)
