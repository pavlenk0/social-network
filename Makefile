install:
	pip install -U pip
	pip install -r requirements.txt

run:
	python manage.py runserver --settings=social_network.settings

migrate:
	python manage.py migrate --settings=social_network.settings

migrations:
	python manage.py makemigrations --settings=social_network.settings

shell:
	python manage.py shell --settings=social_network.settings

flake:
	flake8 .

isort:
	isort -rc --check-only .

fixisort:
	isort -rc -m 3 pages
	isort -rc -m 3 accounts

test:
	python manage.py test --settings=social_network.settings
