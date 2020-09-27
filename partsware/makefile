LOCAL_IP != hostname -I | awk '{$$1=$$1};1'

migrate:
	./manage.py migrate

makemigrations:
	./manage.py makemigrations

run:
	./manage.py runserver $(LOCAL_IP):8000
