from fabric.api import run, env, cd
from fabric.colors import blue
from fabric.context_managers import lcd
from fabric.operations import local

env.hosts = ['184.73.63.7']
env.user = 'ubuntu'
env.path = '/home/ubuntu/wawared/'
env.key_filename = '~/.ssh/wawared.pem'


def deploy():
    push()
    pull()
    install_requirements()
    migrate()
    reload_supervisor()


def push():
    with lcd('~/Workspace/django/wawared'):
        local('git push origin master')


def pull():
    with cd(env.path):
        run('git checkout master')
        result = run('git pull origin master')
        print blue(result)


def migrate():
    with cd(env.path):
        result = run(
            '/home/ubuntu/.virtualenvs/wawared/bin/python '
            'manage.py migrate --settings=settings.production')
        print blue(result)


def install_requirements():
    with cd(env.path):
        result = run(
            '/home/ubuntu/.virtualenvs/wawared/bin/pip '
            'install -r requirements/production.txt')
        print blue(result)

services = ('gunicorn', 'celery')


def reload_supervisor():
    for service in services:
        run('sudo supervisorctl stop %s &> /dev/null' % service)
        run('sudo supervisorctl start %s' % service)
