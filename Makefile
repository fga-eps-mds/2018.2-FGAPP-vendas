default:
	docker build . -t docker-django
	docker run --rm -p 8001:8001 -v `pwd`:"/app" -w "/app" -it docker-django bash