### 1. install uwsgi 
    # sudo apt-get install uwsgi
    # sudo apt-get install uwsgi-plugin-python3

    # nano /etc/uwsgi/apps-available/uwsgi.ini
    # uwsgi --ini fabric_server.ini

    # if use service
    # sudo service uwsgi start
    # sudo service uwsgi reload 
    # sudo cp ./register_service/fabric_server.ini  /etc/uwsgi/apps-available/fabric_server.ini
    # sudo ln -s /etc/uwsgi/apps-available/fabric_server.ini /etc/uwsgi/apps-enabled/
    
    Register
    # sudo uwsgi -i ./register_service/fabric_server.ini 

    Stop
    # sudo uwsgi --stop ./uwsgi.pid
    # https://uiandwe.tistory.com/1210

### 2. install nginx
    # sudo apt-get install nginx
    # sudo cp ./register_service/fabric_server.conf /etc/nginx/sites-available/fabric_server.conf
    # sudo ln -s /etc/nginx/sites-available/fabric_server.conf /etc/nginx/sites-enabled/

    # sudo nginx -t
    # sudo service nginx restart

### https://kibua20.tistory.com/115

# /lib/systemd/system/flask_fabric_server.service
