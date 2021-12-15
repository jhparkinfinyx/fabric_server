## How to 

Install the dependencies:

    # pip install -r requirements.txt


Run the Flask server:

    # FLASK_ENV=development FLASK_APP=app.py flask run -p 9999
    # celery -A app.celery worker --loglevel=info --autoscale=10,3

From another tab, send the image file in a request:

    # curl -X POST -F file=@cat_pic.jpeg http://localhost:9999/predict

    # sudo apt install python-celery-common -y
    # sudo apt-get install redis-server -y

    
## Redis

    $ docker pull redis
    $ docker run --name fabric-redis -d -p 6379:6379 redis


## Mysql

    https://poiemaweb.com/docker-mysql

    $ docker pull mysql
    $ docker run --name mysql-container -v ~/pjh/dyetec/fabric/fabric_server/sql:/sql -e MYSQL_ROOT_PASSWORD=dyetec1124 -d -p 3306:3306 mysql:latest



### MySQL Docker 컨테이너 중지
    $ docker stop mysql-container

### MySQL Docker 컨테이너 시작
    $ docker start mysql-container

### MySQL Docker 컨테이너 재시작
    $ docker restart mysql-container

    $ docker exec -it mysql-container bash
    # mysql -u root -p

    create database fabric_db default character set utf8 collate utf8_general_ci;

## npm

    npm install -g n

    sudo n stable


## Set product(Nginx, uwsgi, flask)
    # ./register_service/REG_SERV_README.md