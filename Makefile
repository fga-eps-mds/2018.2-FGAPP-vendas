default:
	docker build . -t docker-django
	docker run --rm -p 8001:8001 -v `pwd`:"/app" -w "/app" --name order-microservice -it docker-django bash

run:
	docker build . -t docker-django
	docker run --rm -p 8001:8001 -v `pwd`:"/app" -w "/app" --net=backend --name order-microservice -d docker-django bash -c "sh run-django.sh"