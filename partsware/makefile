LOCALIP = $(shell ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1' | awk '{print $1}'| head -n 1)

install:
	sudo apt-get update
	sudo apt-get install -y net-tools
	sudo apt-get install -y python3
	sudo apt-get install -y python3-pip
	pip3 install Django
	pip3 install pillow
	python3 manage.py migrate

migrate:
	python3 manage.py migrate

runserver:
	python3 manage.py runserver $(LOCALIP):8000
