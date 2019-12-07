all: test

test:
	pytest --flake8

black:
	black .

init:
	pip install -r requirements.txt
