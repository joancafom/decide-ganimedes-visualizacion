% prepara el repositorio para su despliegue. 
release: sh -c 'find . -path ./*/migrations/*.py -not -name __init__.py -delete && find . -path ./*/migrations/*.pyc -delete && cd decide && python manage.py makemigrations && python manage.py migrate'
% especifica el comando para lanzar Decide
web: sh -c 'cd decide && gunicorn decide.wsgi --log-file -'