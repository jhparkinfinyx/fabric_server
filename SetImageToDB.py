import os
import cv2
import pymysql

# base_url = "localhost:8080/static/images/"

db = pymysql.connect(host='localhost', user='root', db='fabric_db', password='gktehrm12', charset='utf8')
curs = db.cursor()


path_dir = './static/images'
file_list = os.listdir(path_dir)



def insertToDB(img_path, img_name):
  name, ext = os.path.splitext(img_name)
  # url = base_url + img_name
  sql = "insert into images (name, path) values (%s,%s)"
 
  curs.execute(sql,(name, img_path[2:]))
  rows = curs.fetchall()
  print("rows:", rows)
  db.commit()
  

for img_name in file_list:
  img_path = path_dir + '/' + img_name
  print(img_path)

  insertToDB(img_path, img_name)

db.close()
  

