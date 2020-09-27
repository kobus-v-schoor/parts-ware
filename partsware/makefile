LOCAL_IP != hostname -I | cut -f 1 -d " "

migrate:
	./manage.py migrate

makemigrations:
	./manage.py makemigrations

run:
	./manage.py runserver $(LOCAL_IP):8000
