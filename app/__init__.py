from flask import Flask
from flask_session import Session
from .models import mongo
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os

def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = os.getenv("MONGO_URI") # Read MONGO_URI from the environment
    app.config["MONGO_CONNECT_TIMEOUT_MS"] = 30000
    app.config["MONGO_SOCKET_TIMEOUT_MS"] = 30000
    app.config["SECRET_KEY"] = "0f33ea9b56824840ed1e9af74389a2ad"
    app.config["SESSION_TYPE"] = "filesystem"

    # 使用如下顺序实例化 PyMongo 和 Session 对象
    mongo.init_app(app)
    Session(app)

    from . import views
    app.register_blueprint(views.bp)

    return app