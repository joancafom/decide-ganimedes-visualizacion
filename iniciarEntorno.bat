@echo off
mode con cols=80 lines=20

echo Fichero de inicializacion del entorno de decides

echo Moviendose a decide
CD decide/

echo Realizando makemigrations
python manage.py makemigrations

echo Migrando aplicacion
python manage.py migrate

echo Creando super usuario decide@email.com
python manage.py createsuperuser --email decide@email.com

echo Compilando mensajes de internacionalizacion (i18n)
django-admin compilemessages

echo FIN
pause
exit