from flask import Flask
from flask_session import Session
from .models import mongo

def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = "mongodb://49.232.165.6:3389/topasteit"
    app.config["SECRET_KEY"] = "supersecretkey" # 随意选择一个密钥
    app.config["SESSION_TYPE"] = "filesystem"

    mongo.init_app(app)
    Session(app)

    from . import views
    app.register_blueprint(views.bp)

    return app