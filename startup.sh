#!/bin/bash

if [ $1 ]; then
    if [ $1 == "local" ] || [ $1 == "production" ]; then
        echo "SyncDB.."
        python2 manage.py syncdb --noinput --settings=settings.$1
        echo "Migrate"
        python2 manage.py migrate --settings=settings.$1
        echo "Load data..."
        python2 manage.py loaddata apps/cie/fixtures/*.json --settings=settings.$1
        python2 manage.py loaddata apps/ubigeo/fixtures/*.json --settings=settings.$1
        python2 manage.py loaddata apps/pacientes/fixtures/*.json --settings=settings.$1

        echo "Done!"
    else
        echo "environment name wrong"
    fi
else
    echo "Enter environment name (local, production)"
fi
