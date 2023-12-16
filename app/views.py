from flask import Blueprint, render_template, request, jsonify, session
from .models import mongo
from PIL import Image
from io import BytesIO
import base64
import pytesseract
import uuid
from datetime import timedelta
from random import random
from aip import AipOcr

# 请替换为您的百度 OCR API 密钥
APP_ID = '45118422'
API_KEY = 'iFZhoC6GKbbv7qEOnLr3gnfl'
SECRET_KEY = 'ye30G6Tm0eYKR8gy48ZbeItYH10kDuQK'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

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
    return jsonify(message="保存成功"), 200

@bp.route('/ocr', methods=['POST'])
def ocr():
    image_data = request.form['image'].split(',')[1]
    image = BytesIO(base64.b64decode(image_data))

    # 使用百度 OCR 对图像进行识别
    options = {
        'language_type': 'CHN_ENG',
    }
    response = client.basicGeneral(image.read(), options)

    # 提取识别的文本
    if 'words_result' in response:
        text = '\n'.join([item['words'] for item in response['words_result']])
    else:
        text = ''

    return jsonify(text=text)

# @bp.route('/ocr', methods=['POST'])
# def ocr():
#     image_data = request.form['image'].split(',')[1]
#     image = Image.open(BytesIO(base64.b64decode(image_data)))
#     text = pytesseract.image_to_string(image)
#     return jsonify(text=text)