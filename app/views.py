from flask import Blueprint, render_template, request, jsonify, session
from .models import mongo
from PIL import Image
from io import BytesIO
import base64
import pytesseract
import uuid
from datetime import timedelta
from random import random

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('editor.html')

@bp.route('/save', methods=["POST"])
def save():
    if "sid" not in session:
        session["sid"] = str(random())
    content = request.form["content"]
    posts = mongo.db.posts
    posts.insert_one({"content": content, "session_id": session["sid"]})
    return jsonify(message="Saved successfully"), 200

@bp.route('/ocr', methods=['POST'])
def ocr():
    image_data = request.form['image'].split(',')[1]
    image = Image.open(BytesIO(base64.b64decode(image_data)))
    text = pytesseract.image_to_string(image)
    return jsonify(text=text)