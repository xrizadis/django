run tests:
docker-compose run app sh -c "python manage.py test"

build container
docker-compose build

configure app
docker-compose run app sh -c "python manage.py startapp core"

create migrations
docker-compose run app sh -c "python manage.py makemigrations core"
