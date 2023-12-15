from flask import Flask
from flask_session import Session
from .models import mongo
from flask_pymongo import PyMongo

def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = "mongodb://49.232.165.6:3389/topasteit"
    app.config["MONGO_CONNECT_TIMEOUT_MS"] = 30000
    app.config["MONGO_SOCKET_TIMEOUT_MS"] = 30000
    # app.config["SECRET_KEY"] = "supersecretkey" # 随意选择一个密钥
    # app.config["SESSION_TYPE"] = "filesystem"

    mongo = PyMongo(app, connect=True)
    # 移除mongo.init_app(app)这一行
    Session(app)

    from . import views
    app.register_blueprint(views.bp)

    return app