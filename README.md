# Django Project Template Using SQL

### Version 0.0.1

### Tech Stack

Following is the tech stack being used for demo_sql project:

* [Django 1.8]
* [Django Rest Framework 3.3.3]
* [PostgreSQL]

### Project Setup
* Install virtualenv and virtualenvwrapper:
```sh
$ sudo pip install virtualenv virtualenvwrapper
$ sudo pip install --upgrade pip
```

* Create a backup of the .bashrc file
```sh
$ cp ~/.bashrc ~/.bashrc-org
```

* Create a directory to store all the virtual environments
```sh
$ mkdir ~/.virtualenvs
```

* Set WORKON_HOME to virtual environments directory
```sh
$ export WORKON_HOME=~/.virtualenvs
```

* Open bashrc file
```sh
$ sudo nano ~/.bashrc
```

* Add the following line at the end of bashrc file:
```
. /usr/local/bin/virtualenvwrapper.sh
```

* Re-source terminal using the following command
```sh
$ source ~/.bashrc
```

* Create new virtual environment
```sh
$ mkvirtualenv demo_sql
```

* Activate the virtual environment
```sh
$ workon demo_sql
```

> Gunicorn will be installed while installing requirements

##### Fetching and Prepping the Project
* Clone the project
```sh
$ git clone "https://github.com/eshandas/django_project_template_sql.git"
```

* Rename project directory for consistency and cd
```sh
$ mv demo_sql-api/ demo_sql
$ cd demo_sql
```

> Make sure that correct setting file is pointed in **manage.py** and **wsgi.py** files

> NOTE: Install the following dependencies before installing Pillow:
```sh
$ sudo apt-get install libjpeg-dev libfreetype6-dev zlib1g-dev
```

* Install all the requirements
```sh
$ pip install -r requirements/stage_requirements.txt
```

* Run migrations
```sh
$ python manage.py migrate
```

* Collect all the static files
```sh
$ python manage.py collectstatic
```

* Rebuild Elastic search indexes
```sh
$ python manage.py rebuild_index
```

* Test by running
```sh
$ python manage.py runserver 0.0.0.0:8000
```

##### Setting up Haystack and Elastic Search
* Install Elastic Search, but first update Java
```sh
$ sudo apt-get update
$ sudo apt-get install openjdk-7-jre
$ sudo add-apt-repository -y ppa:webupd8team/java
$ sudo apt-get update
$ sudo apt-get -y install oracle-java8-installer
$ java -version
```

* Setup Elastic Search
```sh
$ wget https://download.elastic.co/elasticsearch/release/org/elasticsearch/distribution/deb/elasticsearch/2.3.3/elasticsearch-2.3.3.deb
$ sudo dpkg -i elasticsearch-2.3.3.deb
```

* Edit the settings file
```sh
$ sudo nano /etc/elasticsearch/elasticsearch.yml
```

* Add node info
```
...
node.name: "demo_sqlNode"
cluster.name: demo_sqlcluster1
...
...
index.number_of_shards: 1
index.number_of_replicas: 0
...
```

* Start Elastic Search
```sh
$ sudo service elasticsearch start
```

* Install Haystack, which is an interface for accessing Elastic Search from Django project
```sh
$ pip install django-haystack
```

* Add Haystack in installed apps
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',

    # Added.
    'haystack',

    # Then your usual apps...
    'blog',
]
```

* Add connection to Elastic Search
```
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'haystack',
    },
}
```

##### Setting up Celery
**Installing a Broker**

Celery requires a message broker to be setup. Celery right now fully supports RabbitMQ and Redis. The other broker supports are not managed actively. In this project we are using Redis as the message broker. It will also work as the backend for Celery. In future we also intend to use Redis for caching.

* Install Redis
```sh
$ sudo apt-get install redis-server
```

* Check if Redis is running
```sh
$ redis-benchmark -q -n 1000 -c 10 -P 5
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
$ pip install django-celery
$ pip install -U celery[redis]
```

* Add tasks file in /utils/ for e.g /utils/email_tasks.py. This holds all the async tasks to be handed to Celery for execution

* Make sure a /diaspo_pay_api/celery.py file is present. This holds all the project level configuration for Celery. The settings are
```
from __future__ import absolute_import
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo_sql.settings.stage')

app = Celery('demo_sql',
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
$ python manage.py migrate
```

* Run Celery server (inside virtualenv) and it will start listening for new tasks
```sh
$ celery -A demo_sql worker -l info
```

* Run Celery beat (inside virtualenv) and it will start scheduling tasks
```sh
$ celery -A demo_sql beat -l info
```
