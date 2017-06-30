# Django Boilerplate

### About

A boilerplate for Django Project. There is sample app named as Posts for reference.

The project is AWS ready and can be deployed in minutes.

The project is also ready for scrapy, haystack, mongodb and celery. These can be configured in minutes as well.

Look at Swagger docs for API details at /api/#/

### Version 0.1

### Tech Stack

Following is the tech stack being used for the project:

* [Django 1.11] - The core Web Framework
* [Django Rest Framework 3.5.3] - For creating REST APIs
* [Sqlite] - As datastore
* [Celery 3.1.23] - A task queue used for async processes and task scheduling
* [Redis 2.8.4] - As message broker, a result backend for Celery and for caching
* [Ubuntu 14.04] - As the operating system
* Gunicorn
* Nginx

### References
##### Installing Nginx in Ubuntu 14.04
* https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-14-04-lts

##### Setting up Django, Gunicorn and Nginx in AWS Ubuntu 14.04
* https://www.digitalocean.com/community/tutorials/how-to-serve-django-applications-with-uwsgi-and-nginx-on-ubuntu-14-04
* http://agiliq.com/blog/2014/08/deploying-a-django-app-on-amazon-ec2-instance/

##### Using Fabric for auto deployment
* https://www.digitalocean.com/community/tutorials/how-to-use-fabric-to-automate-administration-tasks-and-deployments

##### User management in Ubuntu
* https://help.ubuntu.com/lts/serverguide/user-management.html

##### Setting up Elastic Search
* https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-elasticsearch-on-ubuntu-14-04

### Project Setup
* Update ubuntu
```sh
sudo apt-get update
```

* Install python-pip
```sh
sudo apt-get install python-pip python-dev nginx git
sudo apt-get install build-essential libssl-dev libffi-dev
```

* Install virtualenv and virtualenvwrapper:
```sh
sudo pip install virtualenv virtualenvwrapper
sudo pip install --upgrade pip
```

* Create a backup of the .bashrc file
```sh
cp ~/.bashrc ~/.bashrc-org
```

* Create a directory to store all the virtual environments
```sh
mkdir ~/.virtualenvs
```

* Set WORKON_HOME to virtual environments directory
```sh
export WORKON_HOME=~/.virtualenvs
```

* Open bashrc file
```sh
sudo nano ~/.bashrc
```

* Add the following line at the end of bashrc file:
```
. /usr/local/bin/virtualenvwrapper.sh
```

* Re-source terminal using the following command
```sh
source ~/.bashrc
```

* Create new virtual environment
```sh
mkvirtualenv project
```

* Activate the virtual environment
```sh
workon project
```

> Gunicorn will be installed while installing requirements

##### Fetching and Prepping the Project
* Create a parent folder called sites
```sh
mkdir sites && cd sites
```

* Clone the project
```sh
git clone https://eshan_scientist@bitbucket.org/scientisttechnologies/project_api.git
```

* Rename project directory for consistency and cd
```sh
mv project_api/ project && cd project
```

* Point the local settings file in the virtualenv postactivate hook
```sh
deactivate
sudo nano ~/.virtualenvs/project/bin/postactivate
```

* Add the following line
```
...
export DJANGO_SETTINGS_MODULE=main.settings.dev
```

* Remove the pointer once the env is deactivated
```sh
sudo nano ~/.virtualenvs/project/bin/postdeactivate
```

* Add the following line
```
...
unset DJANGO_SETTINGS_MODULE
```


> NOTE: Install the following dependencies before installing Pillow:


```sh
sudo apt-get install libjpeg-dev libfreetype6-dev zlib1g-dev
```

* Install all the requirements
```sh
workon project
pip install -r requirements/server.txt
```
**NOTE:** If scipy installation throws MemoryError, add swap memory. Install htop and check
```sh
sudo /bin/dd if=/dev/zero of=/var/swap.1 bs=1M count=1024
sudo /sbin/mkswap /var/swap.1
sudo /sbin/swapon /var/swap.1
sudo apt-get install htop
```

* Run migrations
```sh
python manage.py migrate
```

* Collect all the static files
```sh
python manage.py collectstatic
```

* Test by running
```sh
python manage.py runserver 0.0.0.0:8000
```

##### Setting up Celery
**Installing a Broker**

Celery requires a message broker to be setup. Celery right now fully supports RabbitMQ and Redis. The other broker supports are not managed actively. In this project we are using Redis as the message broker. It will also work as the backend for Celery. In future we also intend to use Redis for caching.

* Install Redis
```sh
sudo apt-get install redis-server
```

* Check if Redis is running
```sh
redis-benchmark -q -n 1000 -c 10 -P 5
```

```
PING_INLINE: 200000.00 requests per second
PING_BULK: 200000.00 requests per second
SET: 499999.97 requests per second
GET: 499999.97 requests per second
INCR: 499999.97 requests per second
LPUSH: 499999.97 requests per second
LPOP: 499999.97 requests per second
SADD: 499999.97 requests per second
SPOP: 499999.97 requests per second
LPUSH (needed to benchmark LRANGE): 333333.34 requests per second
LRANGE_100 (first 100 elements): 90909.09 requests per second
LRANGE_300 (first 300 elements): 21276.60 requests per second
LRANGE_500 (first 450 elements): 13888.89 requests per second
LRANGE_600 (first 600 elements): 10869.57 requests per second
MSET (10 keys): 166666.67 requests per second
```

* Install Celery (If you ran pip requirements, this would already have been installed)
```sh
pip install django-celery
pip install -U celery[redis]
```

* Add tasks file in /utils/ for e.g /utils/email_tasks.py. This holds all the async tasks to be handed to Celery for execution

* Make sure a /main/celery.py file is present. This holds all the project level configuration for Celery. The settings are
```
from __future__ import absolute_import
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings.stage')

app = Celery('main',
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/0',
             include=['utils.indexing_tasks', 'utils.email_tasks'])

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')


# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))

CELERY_TIMEZONE = 'UTC'
```

* Also add "djcelery" in installed apps
```
INSTALLED_APPS = [
    ...
    'djcelery',
    ...
]
```

* Add the following at the bottom of the settings.py
```
# Celery related settings
# task result life time until they will be deleted
CELERY_TASK_RESULT_EXPIRES = 7 * 86400  # 7 days
# needed for worker monitoring
CELERY_SEND_EVENTS = True
# where to store periodic tasks (needed for scheduler)
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"

# add following lines to the end of settings.py
import djcelery
djcelery.setup_loader()
```

* Run migrate and it will create 
```sh
python manage.py migrate
```

* Run and test Celery worker (inside virtualenv) and it will start listening for new tasks
```sh
celery -A main worker -l info
```

* Run and test Celery beat (inside virtualenv) and it will start scheduling tasks
```sh
celery -A main beat -l info
```

* Test if Gunicorn can serve the Django pages
```sh
/home/ubuntu/.virtualenvs/project/bin/gunicorn --bind 0.0.0.0:8000 main.wsgis.dev:application
```

* Close server and deactivate the virtualenv

##### Install Upstart for 16.04 (Ignore if using Ubuntu 14.04)
Upstart has been removed after 14.04. Install it by
```sh
sudo apt-get install upstart-sysv
```

>NOTE: Installing Upstart removes the default Systemd

* Update the Ubuntu system to reflect the changes

```sh
sudo update-initramfs -u
```

##### Setting up Gunicorn
* Create and open an Upstart file for Gunicorn with sudo privileges

```sh
sudo nano /etc/init/gunicorn.conf
```

* Configure the Upstart file

```
description "Gunicorn application server handling Project APIs"

start on runlevel [2345]
stop on runlevel [!2345]

respawn
setuid ubuntu
setgid www-data
chdir /home/ubuntu/sites/project

exec /home/ubuntu/.virtualenvs/project/bin/gunicorn --workers 3 --bind unix:/home/ubuntu/sites/project.sock main.wsgis.dev:application
```

>NOTE: For more details, read the link given in the References section

* Start the Gunicorn service

```sh
sudo service gunicorn start
```
>NOTE: Check error log by **sudo tail -f /var/log/upstart/gunicorn.log**
* Reboot the system

##### Setting up Nginx
* Start by creating and opening a new server block in Nginx's sites-available directory

```sh
sudo nano /etc/nginx/sites-available/project
```

* Add the following configuration in the server block:

```
server {
    listen 80 default_server;

    location = /favicon.ico { access_log off; log_not_found off; }

    # Point to the static folder where static files are collected
    # Refer settings/base.py
    location /static/ {
        root /home/ubuntu/sites/project;
    }

    # Point to the media folder where user media files are uploaded
    # Refer settings/base.py
    location /media/ {
        root /home/ubuntu/sites/project;
    }

    # Point to the socket being used to talk to Gunicorn
    location / {
        include proxy_params;
        client_max_body_size 50m;
        proxy_pass http://unix:/home/ubuntu/sites/project.sock;
    }
}
```

* Enable the file by linking it to the sites-enabled directory:

```sh
sudo ln -s /etc/nginx/sites-available/project /etc/nginx/sites-enabled
```

* Remove the default file from "sites-enabled"

```sh
sudo rm /etc/nginx/sites-available/default
sudo rm /etc/nginx/sites-enabled/default
```

* Test your Nginx configuration for syntax errors by typing:

```sh
sudo nginx -t
```

* If no errors are reported, go ahead and restart Nginx by typing:

```sh
sudo service nginx restart
```
>NOTE: Check out the log file by **sudo tail -f /var/log/nginx/error.log**

##### Setup Supervisord

* Create supervisor config file if it doesn't exist (in project root folder)

```sh
echo_supervisord_conf > supervisord.conf
```

* Unlink supervisord config for celery after cleaning. Go to project root and execute the following

```sh
sudo unlink /var/run/supervisor.sock
sudo unlink /tmp/supervisor.sock
nano supervisord.conf
```

* Add program setting at the bottom of supervisord.conf

* This is the following configuration file for supervisor

```
.
.
.
[supervisord]
logfile=/home/ubuntu/sites/logs/supervisord.log ; (main log file;default $CWD/supervisord.log)
logfile_maxbytes=50MB        ; (max main logfile bytes b4 rotation;default 50MB)
logfile_backups=10           ; (num of main logfile rotation backups;default 10)
loglevel=info                ; (log level;default info; others: debug,warn,trace)
pidfile=/tmp/supervisord.pid ; (supervisord pidfile;default supervisord.pid)
nodaemon=false               ; (start in foreground if true;default false)
minfds=1024                  ; (min. avail startup file descriptors;default 1024)
minprocs=200                 ; (min. avail process descriptors;default 200)
.
.
.
[program:celeryd]
command=/home/ubuntu/.virtualenvs/project/bin/celery -A main worker
stdout_logfile=/home/ubuntu/sites/logs/celeryd.log
stdout_logfile_maxbytes=1MB
stdout_logfile_backups=10
stdout_capture_maxbytes=1MB
stdout_events_enabled=true
stderr_logfile=/home/ubuntu/sites/logs/celeryd_err.log
stderr_logfile_maxbytes=1MB
stderr_logfile_backups=10
stderr_capture_maxbytes=1MB
stderr_events_enabled=true
autostart=true
autorestart=true
startsecs=4
startretries=5
stopwaitsecs=10

[program:beatd]
command=/home/ubuntu/.virtualenvs/project/bin/celery -A main beat
stdout_logfile=/home/ubuntu/sites/logs/beatd.log
stdout_logfile_maxbytes=1MB
stdout_logfile_backups=10
stdout_capture_maxbytes=1MB
stdout_events_enabled=true
stderr_logfile=/home/ubuntu/sites/logs/beatd_err.log
stderr_logfile_maxbytes=1MB
stderr_logfile_backups=10
stderr_capture_maxbytes=1MB
stderr_events_enabled=true
autostart=true
autorestart=true
startsecs=4
startretries=5
stopwaitsecs=10

[program:celerycamd]
command=/home/ubuntu/.virtualenvs/project/bin/python manage.py celerycam
stdout_logfile=/home/ubuntu/sites/logs/celerycamd.log
stdout_logfile_maxbytes=1MB
stdout_logfile_backups=10
stdout_capture_maxbytes=1MB
stdout_events_enabled=true
stderr_logfile=/home/ubuntu/sites/logs/celerycamd_err.log
stderr_logfile_maxbytes=1MB
stderr_logfile_backups=10
stderr_capture_maxbytes=1MB
stderr_events_enabled=true
autostart=true
autorestart=true
startsecs=4
startretries=5
stopwaitsecs=10

# An email will be sent if a process has stopped
[eventlistener:stopped]
command=/home/ubuntu/.virtualenvs/project/bin/python manage.py runscript utils.supervisord_events.stopped_event
events=PROCESS_STATE_STOPPED

# An email will be sent if a process could not start after max tries for restart
[eventlistener:fatal]
command=/home/ubuntu/.virtualenvs/project/bin/python manage.py runscript utils.supervisord_events.fatal_event
events=PROCESS_STATE_FATAL

# An email will be sent if a process has exited
[eventlistener:exited]
command=/home/ubuntu/.virtualenvs/project/bin/python manage.py runscript utils.supervisord_events.exited_event
events=PROCESS_STATE_EXITED
```

* Create a folder to hold the log files

```sh
mkdir /home/ubuntu/sites/logs/
```

* Start all Supervisord processes

```sh
supervisord
```

##### Reset processes
```sh
sudo service gunicorn restart
sudo service nginx restart
supervisorctl restart celeryd
supervisorctl restart beatd
supervisorctl restart celerycamd
```
