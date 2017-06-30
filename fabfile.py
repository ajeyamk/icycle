# Fabfile to:
#    - update the remote system(s) 
#    - download and install an application

# Import Fabric's API module
from fabric.api import *


STAGES = {
    'production': {
        'hosts': ['ec2-18-220-53-253.us-east-2.compute.amazonaws.com'],
        'code_dir': '~/sites/icycle/',
        'code_branch': 'master',
        'virtual_env': '. /usr/local/bin/virtualenvwrapper.sh; workon icycle',
        'user': 'ubuntu',
    },
}

LOCAL_PEM_PATH = '/home/ymedia/Downloads/hackathon/'
FIXTURE_DIR = '/home/yml/Documents/Stuff/Project/fixtures/'
DOCS_DIR = '/home/yml/Documents/Stuff/Project/_docs/sphinx/'


def stage_set(stage_name='dev'):
    env.stage = stage_name
    for option, value in STAGES[env.stage].items():
        setattr(env, option, value)


def dev():
    # Add key to ssh
    local('ssh-add %s%s' % (LOCAL_PEM_PATH, 'dev.pem'))
    stage_set('dev')


def staging():
    # Add key to ssh
    local('ssh-add %s%s' % (LOCAL_PEM_PATH, 'staging-project.pem'))
    stage_set('staging')


def production():
    # Add key to ssh
    local('ssh-add %s%s' % (LOCAL_PEM_PATH, 'prod-project.pem'))
    stage_set('production')


def print_env_details(env, current_command):
    print '\n\n'
    print '...........................................'
    print 'Command: %s' % current_command
    print 'Updating Server: %s' % env.stage
    print 'Hosts: %s' % env.hosts
    print 'Host User: %s' % env.user
    print 'Code Branch: %s' % env.code_branch
    print '...........................................'
    print '\n\n'


def print_banner(messages):
    print '\n\n'
    print '...........................................'
    if type(messages) == list:
        for message in messages:
            print message
    else:
        print messages
    print '...........................................'
    print '\n\n'


def update():
    print_env_details(env, 'update')
    # local('python manage.py test')
    with cd(env.code_dir):
        with prefix(env.virtual_env):
            run('git pull origin %s' % env.code_branch)
            run('python manage.py migrate')
            run('python manage.py collectstatic --noinput')
            # run('python manage.py test')
            run('sudo service gunicorn restart')
            run('sudo service nginx restart')
            # run('supervisorctl restart celeryd')
            # run('supervisorctl restart beatd')
            # run('supervisorctl restart celerycamd')


def deploy():
    print_env_details(env, 'deploy')
    # local('python manage.py test')
    with cd(env.code_dir):
        with prefix(env.virtual_env):
            run('git pull origin %s' % env.code_branch)
            run('pip install -r requirements/server.txt')
            run('python manage.py migrate')
            run('python manage.py collectstatic --noinput')
            # run('python manage.py test')
            run('sudo service gunicorn restart')
            run('sudo service nginx restart')
            run('supervisorctl restart celeryd')
            run('supervisorctl restart beatd')
            run('supervisorctl restart celerycamd')


def dumpdata():
    print_banner('Dumping data to %s' % FIXTURE_DIR)
    local('python manage.py dumpdata appauth > fixtures/appauth.json')


def loaddata():
    print_banner('Loading data from %s' % FIXTURE_DIR)
    local('python manage.py loaddata fixtures/appauth.json')


def resetdb():
    print_banner('Resetting the database')
    local('sudo rm db.sqlite3')
    # local('python manage.py makemigrations')
    local('python manage.py migrate')
    loaddata()


def generate_docs():
    print_banner('Creating documentations')
    with cd(DOCS_DIR):
        local('make html')
