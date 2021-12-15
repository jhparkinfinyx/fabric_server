import pymysql


class SingletonInstane:
  __instance = None
  def __init__(self):  
    self.db = None

  @classmethod
  def openDB(cls):
    cls.db = pymysql.connect(
      host='localhost', 
      user='root', 
      db='fabric_db', 
      password='dyetec1124', 
      charset='utf8'
    )

  @classmethod
  def __getInstance(cls):
    return cls.__instance

  @classmethod
  def instance(cls, *args, **kargs):
    cls.__instance = cls(*args, **kargs)
    cls.instance = cls.__getInstance
    return cls.__instance

  

class DBController(SingletonInstane):

  @classmethod
  def getImages(cls, sql, data):
    cls.openDB()
    curs = cls.db.cursor()
    curs.execute(sql, data)
    # dbController.mail_send_process()
    rows = curs.fetchall()
    # print(rows)
    cls.db.close()
    
    return rows
  
  @classmethod
  def setImages(cls, sql, data):
    cls.openDB()
    curs = cls.db.cursor()
    curs.execute(sql, data)
    # dbController.mail_send_process()
    curs.fetchall()
    # print(rows)
    cls.db.commit()
    cls.db.close()

    return

  @classmethod
  def close(cls):
    cls.db.close()


  



