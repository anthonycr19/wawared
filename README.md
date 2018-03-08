# THIS README ASSUMES THE FOLLOWING:
- **git** is installed and this repository has been downloaded, it's location is noted on the following item. 
  Repository download is usually handled by git, but it could have been copied with zip, as long as no location 
  changes were made.
- Directory used is /opt/apps/app_wawared. This is the repository directory.
- Proper language and timezone are configured on the server.

## Install:

```sh
sudo apt-get update
sudo apt-get install -y python-pip python-virtualenv libjpeg-dev libfreetype6  libfreetype6-dev zlib1g-dev libpq-dev python-dev libffi-dev git build-essential libssl-dev libffi-dev
sudo apt-get install -y redis-server
sudo apt-get install -y postgresql postgresql-contrib postgresql-client
sudo apt-get install -y nginx supervisor
sudo apt-get install -y openjdk-7-jre openjdk-7-jre
```

- Create virtualenv directory: `mkdir env`
- Create environment: `virtualenv --no-site-package --distribute env`
- Load virtualenv: `source env/bin/activate`
- Install dependencies: `pip install -r requirements/local.txt` (for development) //as of last commit (2016-11-03) doesn't work
- Install dependencies: `pip install -r requirements/production.txt` (for production)
- Create database user and set a password and create a db for the application

```sh
sudo su - postgres
createuser --interactive wawared ;give no permissions
psql
 ALTER USER wawared WITH PASSWORD 'wawareddbpass';
 CREATE DATABASE wawareddb WITH OWNER wawared;
 \q
exit
```

- Create .env file: `touch .env`
- Edit settings params in .env file with the below values (customize according to your needs, default sample works on most occasions):

```sh
SECRET_KEY="THIS_MUST_NOT_BE_EMPTY"
DOMAIN="http://wawared.minsa.gob.pe"
DB_NAME="wawareddb"
DB_USER="uwawared_minsa"
DB_PASSWORD="XXXXXXX"
DB_HOST="localhost"
DB_PORT="5432"

EMAIL_HOST="smtp.gmail.com"
EMAIL_HOST_USER="*****@gmail.com"
EMAIL_HOST_PASSWORD="*****"
EMAIL_HOST_PORT="587"

BROKER_URL="redis://localhost:6379/"
BROKER_RESULT_BACKEND="redis://localhost:6379/"
STATIC_URL="/static/"
MEDIA_URL="/media/"

SETTINGS="settings.local"
DJANGO_SETTINGS_MODULE="settings.local"

JASPER_URL="http://10.10.3.153:8080/jasperserver/rest_v2/reports"
JASPER_USER="*****"
JASPER_PASSWORD="*****"
JASPER_PATH="/Reports/wawared"

URL_LOGIN_SERVER="http://login.minsa.gob.pe/"
LOGIN_DOMAIN=".minsa.gob.pe"
APP_IDENTIFIER="pe.gob.minsa.wawared"
SMS_URL="http://api.holacliente.com/api/sendsms/xml"
API_SYNCHRONIZE_MIRTH=""
DSN_URL=""
CITA_API_URL="http://devcitas.minsa.gob.pe/"
CITA_CLIENT_ID=""
CITA_CLIENT_SECRET=""

MPI_API_HOST="http://mpi.minsa.gob.pe"
MPI_API_TOKEN="******"
EXSER_HOST="sms.minsa.gob.pe"
EXSER_TOKEN="***********"
CLAVE_SIS_TRAMA="*******"
FIRMA_JS_URL = "************"
```

- Make migrations/(estructura to database): python manage.py migrate

If that is not working, try:

```sh
./manage.py migrate cie ubigeo  
./manage.py migrate establecimientos  
./manage.py migrate perfiles  
./manage.py migrate pacientes  
./manage.py migrate embarazos  
./manage.py migrate controles  
./manage.py migrate citas  
```

- Load data:

```sh
python manage.py loaddata apps/ubigeo/fixtures/*.json
python manage.py loaddata apps/pacientes/fixtures/*.json
python manage.py loaddata apps/controles/fixtures/*.json
```

- Collect static (add static django): `python manage.py collectstatic --noinput`  
- Change media directory owner to the user who runs gunicorn: //should be run after django creates media folder later

```sh
sudo chown -R www-data:www-data media/
```

## Setup and install jasperserver:

* *Optional*, do this from another directory, in order not to make changes to the repo: cd ~  
- Download installer:

```sh
wget -c http://downloads.sourceforge.net/project/jasperserver/JasperServer/JasperReports%20Server%20Community%20Edition%205.6.0/jasperreports-server-cp-5.6.0-linux-x64-installer.run
```

- Make installer executable

```sh
chmod a+x jasperreports-server-cp-5.6.0-linux-x64-installer.run
```

- Run installer

```sh
sudo ./jasperreports-server-cp-5.6.0-linux-x64-installer.run
```

* Choose custom install  
* Choose to install at default directory (/opt/jasperreports-server-cp-5.6.0/)  
* Choose to use bundled tomcat  
* Choose to use default port (8080) for tomcat  
* Choose to use bundled postgresql  
* Choose to use different port, recommended (5435)  
* Choose to not go to the page offered.  

- After installation is complete, run the client

```sh
sudo /opt/jasperreports-server-cp-5.6.0/ctlscript.sh start
``` 

-Test functionality then stop the jasperserver

```sh
sudo /opt/jasperreports-server-cp-5.6.0/ctlscript.sh stop
```

- After verification copy initjasperserver to /etc/init.d/ and give it 755 permissions:

```sh
sudo cp samples/initjasper.txt /etc/init.d/jasperserver
sudo chmod 755 /etc/init.d/jasperserver
sudo service jasperserver start
```

- To make it run at server start-up, do:

```sh
sudo update-rc.d jasperserver defaults
```

- Run Django: python manage.py runserver

Final pip freeze:

```
Django==1.7.11
Pillow==3.2.0
XlsxWriter==0.8.7
amqp==1.4.9
anyjson==0.3.3
argparse==1.2.1
beautifulsoup4==4.4.1
billiard==3.3.0.18
celery==3.1.16
cffi==1.6.0
cryptography==1.3.2
decorator==4.0.9
diff-match-patch==20110725.1
django-celery==3.1.16
django-dotenv==1.3.0
django-flat-theme==1.1.1
django-htmlmin==0.6.3
django-import-export==0.4.2
django-session-security==2.3.1
django-smart-selects==1.2.2
easy-thumbnails==1.5
ecdsa==0.13
enum34==1.1.6
funcsigs==1.0.0
gunicorn==18.0
html5lib==0.999
idna==2.1
invoke==0.8.2
ipaddress==1.0.16
ipython==4.1.2
ipython-genutils==0.1.0
kombu==3.0.35
matplotlib==1.4.0
mock==2.0.0
nose==1.3.7
numpy==1.11.0
ordereddict==1.1
paramiko==1.16.0
pathlib2==2.1.0
pbr==1.8.1
pexpect==4.0.1
pickleshare==0.7.2
plivo==0.11.0
psycopg2==2.5.1
ptyprocess==0.5.1
pyasn1==0.1.9
pycparser==2.14
pycrypto==2.6.1
pyjasperclient==0.2.3
pyparsing==2.1.1
python-dateutil==2.5.2
pytz==2016.3
raven==4.0.4
redis==2.8.0
reportlab==3.2.0
requests==2.5.0
simplegeneric==0.8.1
simplejson==3.3.2
six==1.10.0
sqlparse==0.1.10
suds==0.4
tablib==0.11.2
traitlets==4.2.1
wsgiref==0.1.2
```

# Configure gunicorn, supervisor and nginx

For nginx:

- Create a configuration file on /etc/nginx/sites-available/ named `vih.com.conf` and copy the sample configuration file nginx.vih.conf.samlple content's into it (modify if required).

```sh
sudo cp samples/wawared.nginx.conf.sample /etc/nginx/sites-available/wawared.com.conf
```

- Create simbolyc link for the new configuration file and reload nginx:
- Optional, validate nginx configuration, delete nginx default configuration file symbolic link.

```sh
sudo ln -s /etc/nginx/sites-available/wawared.com.conf /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo nginx -s reload
```

For gunicorn:

- Create a configuration file on settings/ named `gunicorn.conf.py`.
- Copy sample configuration file gunicorn.conf.py.sample content's into the new file.

```sh
sudo cp samples/gunicorn.conf.py.sample settings/gunicorn.conf.py
```

For supervisor:

- Create a configuration file on /etc/supervisor/conf.d/ named `wawared.conf`, and copy the sample configuration file supervisord.conf.sample content's into it.
- Also create logs directory

```sh
sudo cp samples/wawared.supervisor.conf.sample /etc/supervisor/conf.d/wawared.conf
mkdir logs
```

- Then read new configurations: (assuming program name wawared)

```sh
sudo supervisorctl reread
sudo supervisorctl update wawared
sudo supervisorctl restart wawared
```

- Se actualizó el REQUESTS pip install -U requests

La variable de entorno FIRMA_JS_URL es requerida para la firma electronica
