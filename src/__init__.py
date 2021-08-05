from flask import Flask

from extensions import db
from src.endpoints.deals import deal_bp
from src.endpoints.index import index_bp
from src.endpoints.login import user_bp


def create_app(config_file="settings.py"):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    app.secret_key = app.config["SECRET_KEY"]
    db.init_app(app)
    app.debug = True
    return app


app = create_app()
app.register_blueprint(index_bp)
app.register_blueprint(user_bp)
app.register_blueprint(deal_bp)
