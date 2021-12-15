import os
import io
import json
import time
import atexit
import base64

from PIL import Image


from torchvision import models
import torchvision.transforms as transforms
from PIL import Image
from flask import Flask, jsonify, request, render_template, send_from_directory

from werkzeug.utils import secure_filename

from flask_cors import CORS
import pymysql
# from celery import Celery

from modules.db import DBController

from modules.similarity_model import similarity

from model.similarity.dyetec_similar_test_211213 import run as similarity_run
from model.gan.cCycle_test import run as gan_run
from model.similarity.get_similarity_vector import run as vector_run

UPLOAD_FOLDER = './static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__, static_url_path='/static')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)

app.config['JSON_AS_ASCII'] = False

# celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
# celery.conf.update(app.config)

# CORS(app)
# CORS(app, resources={r'*': {'origins': 'http://localhost:3000'}}, supports_credentials=True)
CORS(app, resources={r'*': {'origins': '*'}}, supports_credentials=True)

imagenet_class_index = json.load(open('imagenet_class_index.json'))
model = models.densenet121(pretrained=True)
model.eval()

# # create DB
db = DBController.instance()

def transform_image(image_bytes):
    my_transforms = transforms.Compose([transforms.Resize(255),
                                        transforms.CenterCrop(224),
                                        transforms.ToTensor(),
                                        transforms.Normalize(
                                            [0.485, 0.456, 0.406],
                                            [0.229, 0.224, 0.225])])
    image = Image.open(io.BytesIO(image_bytes))
    return my_transforms(image).unsqueeze(0)

# test
def get_prediction(image_bytes):
    tensor = transform_image(image_bytes=image_bytes)
    outputs = model.forward(tensor)
    _, y_hat = outputs.max(1)
    predicted_idx = str(y_hat.item())
    return imagenet_class_index[predicted_idx]


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @celery.task #(bind=True)
# def asyncInferenceSimilerModel(data):
#     print("asyncInferenceSimilerModel()")
    
#     # with app.app_context():
#         # 모델 작업 수행
    
#     # string to bytes
#     img_bytes = base64.b64decode(data['img_str'])
    
#     # model work
#     rows = similarity_run(img_bytes, data['img_rows'])

#     # # open image
#     # image = Image.open(io.BytesIO(img_bytes))
#     # image.show()

#     # # test work
#     # class_id, class_name = get_prediction(image_bytes=img_bytes)
#     # time.gmtime(1000)
    
#     return rows # data['img_rows']

# @celery.task
# def asyncQeruyDB(sql):
#     print("asyncQeruyDB()")
#     print(5)
#     rows =getImages(sql)
#     print(6)
#     return rows
 
    
'''
    Name : Create drape images
    Param : [number, ...]
    return [bytes, bytes]
'''
@app.route('/api/drape', methods=['post'])
def image_drape():
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        # data = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37]

       
        img1, img2 = gan_run(data)
        res1 = base64.b64encode(img1)
        res2 = base64.b64encode(img2)
        print("response:",[res1.decode("utf-8"), res2.decode("utf-8")])
        # return str(image)
        return jsonify([res1.decode("utf-8"), res2.decode("utf-8")])
    

'''
    Name : Search similarity images
    Param : file(image)
    return [{img_row}, ...]
'''  
@app.route('/api/similarity', methods=['POST'])
def image_similarity():
    if request.method == 'POST':
        file = request.files['file']

        # bytes to string
        img_str = base64.b64encode(file.read())
        img_str = img_str.decode('utf-8')
        # print("img_str: ", img_str[:100])

        sql = "select * from images"
        
        # task = asyncQeruyDB.delay(sql)
        # img_rows = task.get()
        
        rows = db.getImages(sql, ())
        img_rows = rows
        # print(img_rows)

        data = {
            'img_str': img_str, # 이미지 파일 자체 데이터
            'img_rows': img_rows # DB에서 불러온 이미지 테이블 데이터(id,이름,위치,백터값,시간정보)
        }

        # # send to celery worker
        # task = asyncInferenceSimilerModel.delay(data)
        # response = task.get()

        response = similarity_run(base64.b64decode(data['img_str']), data['img_rows'])

        print(response)
        return jsonify([response])


'''
    Name : Upload images
    Param : file(image), fileName
    return isSuccess
'''  
@app.route('/api/upload', methods=['POST'])
def image_upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file part')
            return jsonify({"isSuccess": 0, "message": "파일이 존재하지 않습니다."})
        
        file = request.files['file']
        
        # bytes to string
        img_str = base64.b64encode(file.read())
        img_str = img_str.decode('utf-8')
        # print("img_str: ", img_str[:100])
        img_bytes = base64.b64decode(img_str)
        
        if file.filename == '':
            print('No selected file')
            return jsonify({"isSuccess": 0, "message": "파일이 존재하지 않습니다."})
        

        file_name = file.filename
        # print('file_name: ', file_name)
        
        
        
        if not file or not allowed_file(file_name):
             return jsonify({"isSuccess": 0, "message": "파일이 존재하지 않습니다."})
         
        filename = secure_filename(file_name)
        # print('filename: ', filename)
        
        name = os.path.splitext(filename)[0]
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)[2:]
        vector = vector_run(img_bytes)
        # print(path)
        
        # dup check
        rows = db.getImages("select * from images where name=%s", (name))
        # print("rows.length: ", len(rows))
        if len(rows) > 0 :
            return jsonify({"isSuccess": 0, "message": "파일이 이미 존재합니다."})
        
        file.seek(0)
        file.save(path)
        
        res = db.setImages("insert into images (name, path, vector) values (%s,%s,%s)", (name, path, str(vector)))
        print(res)

        # response = similarity_run(base64.b64decode(data['img_str']), data['img_rows'])

        # print(response)
        return jsonify({"isSuccess": 1, "message": "파일 업로드 성공！", "img": [[], 1, name, path] })
    
    

@app.route('/static/images/<image_file>')
def image(image_file):
    # print(image_file)
    return send_from_directory('./static/images', image_file)
    # return render_template('img.html', image_file='images/'+image_file)

# @app.route('/static/images')
# def image():
#     name = request.args.get('name', default = '', type = str)
#     print(name)
#     return send_from_directory('./static/images', name)


@app.route("/api/images", methods=['GET']) 
def images(): 
    rows = db.getImages("select vector, id, name, path from images ORDER BY id DESC", ())
    return jsonify(rows)


@app.route('/api/image', methods=['POST']) 
def delete_image(): 
    if request.method == 'POST':
        data = request.form
        print(data.get('id'))
        target_id = data.get('id')
        
        # get db info
        rows = db.getImages("select id, name, path from images where id=%s", (target_id))
        print(rows)
        filename = os.path.basename(rows[0][2])
        
        # remove db info
        db.setImages("delete from images where id=%s", (target_id))
        
        # # remove static file
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)[2:]
        os.remove(path)
        
        return jsonify({"isSuccess": 1, "message": "파일이 삭제 되었습니다."})
    
@app.route("/") 
def home(): 
    return "Dive Fabric"

if __name__ == '__main__':
    # app.run(host='0.0.0.0')
    app.run(host='0.0.0.0', port=9999, debug=True)
    # app.run(host='127.0.0.1', port=8080)


# def cleanup():
#     try:
#         # db.close()
#         # print("db closed!")
#     except Exception:
#         pass
# atexit.register(cleanup)


####