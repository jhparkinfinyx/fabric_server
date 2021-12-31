import json
import pymysql

db = pymysql.connect(
    host='localhost', 
    user='root', 
    db='fabric_db', 
    password='dyetec1124', 
    charset='utf8'
  )



with open("./similarity_4045_resize.json") as json_file:
  json_data = json.load(json_file)

  print(json_data[0]['name'])

  curs = db.cursor()

  for v in json_data:
    data = (str(v['vector'][0]), str(v['vector'][1]), v['name'])
    sql = 'UPDATE images SET vector=%s, vector2=%s WHERE name=%s'

    curs.execute(sql, data)
    # print(type(str(v['vector'])))

  sql = "select * from images"
  curs.execute(sql)
  
  rows = curs.fetchall()
  print(rows)

  db.commit()
  db.close()

