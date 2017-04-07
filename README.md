# Project API local setup

### Version 0.1

### About

A boilerplate for Django Project with SQL. There is sample app named as Posts for reference.

The project is AWS ready and can be deployed in minutes.

The project is also ready for scrapy, haystack, mongodb and celery. These can be configured in minutes as well.

Look at Swagger docs for API details at /api/#/

### Posts App
A sample app for reference, which covers all the major aspects of Django development.

#### Structure
* **models.py:** Where all models live.
* **serializers.py:** Django Rest Framework serializers.
* **api_views.py:** Where all the web APIs live.
* **api_urls.py:** Router to server the API Views.
* **views.py:** Where all views for web pages live.
* **urls.py:** Router for web pages views.
* **templates/posts:** HTML templates for the views.
* **admin.py:** All Django admin related settings.
* **constants.py:** All app related constants live here.

#### Standards
* PEP8 compatible coding style.
* Doc strings for all the modules and their members. These doc strings are read by Sphinx and Swagger to create documentations.
* DRY - All constants are kept in one place. Big complicated logic is broken down into small pieces/methods.

### Tech Stack

Following is the tech stack being used for main project:

* [Django 1.8] - The core Web Framework
* [Django Rest Framework 3.3.3] - For creating REST APIs
* [Sqlite] - As datastore
* [Celery 3.1.23] - A task queue used for async processes and task scheduling
* [Redis 2.8.4] - As message broker, a result backend for Celery and for caching

### Project Setup
* Update ubuntu
```sh
sudo apt-get update
```

* Install python-pip
```sh
sudo apt-get install python-pip python-dev git
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
export DJANGO_SETTINGS_MODULE=main.settings.local
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

* Test by running
```sh
python manage.py runserver
```

##### Setting up Haystack and Elastic Search
Not required for now. Check _docs in case if needed.

##### Setting up Celery
Not required for now. Check _docs in case if needed.

##### Setting up Gunicorn
Not required for now. Check _docs in case if needed.

##### Setting up Nginx
Not required for now. Check _docs in case if needed.

##### Setup Supervisord
Not required for now. Check _docs in case if needed.

##### Documentation
This application uses Sphinx for complete documentation and Django Rest Swagger for documenting APIs.

* Sphinx: Please have a look at /_docs/sphinx/_build/html/index.html for Sphinx documentation.

* Swagger: Please visit 127.0.0.1:8000/api/ for Swagger documentation