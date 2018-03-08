#!/usr/bin/env python
import os
import sys
from django.core.exceptions import ImproperlyConfigured


def load_env_vars():
    try:
        with open('.env') as env_file:
            content = env_file.read()
    except IOError:
        raise ImproperlyConfigured('missed .env file')

    for line in content.splitlines():
        line = line.split('=')
        line = map(lambda x: x.replace('\"', ''), line)
        key, value = line[0], ''.join(line[1:])
        os.environ.setdefault(key, value)

if __name__ == "__main__":
    load_env_vars()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", os.environ['SETTINGS'])

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
