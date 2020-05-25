run tests:
docker-compose run --rm app sh -c "python manage.py test && flake8"

build container
docker-compose build

configure app
docker-compose run app sh -c "python manage.py startapp core"

create migrations
docker-compose run app sh -c "python manage.py makemigrations core"

start
docker-compose up

create app
docker-compose run app sh -c "python manage.py startapp info"
