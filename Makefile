PROJECT_NAME=project
MANAGE=python manage.py
SETTINGS=--settings=$(PROJECT_NAME).settings.test

DOCKER_POSTGRES_REPO=postgres
DOCKER_POSTGRES_TAG=9.3


.PHONY: all test coverage clean requirements requirements-dev setup-test \
	docker-check db-restore db-prompt migrate \
	superuser

all: coverage

test:
	$(MANAGE) test $(SETTINGS)

coverage:
	$(MANAGE) test $(SETTINGS) && coverage html

clean:
	rm -rf .coverage cover
	find . -name '*.pyc' -exec rm '{}' ';'

requirements-dev:
	@if [ -z $$VIRTUAL_ENV ]; then \
		echo "You should probably install stuff in virtualenv instead."; \
		exit 1; \
	else \
		pip install -r requirements/dev.txt; \
	fi

requirements:
	@if [ -z $$VIRTUAL_ENV ]; then \
		echo "You should probably install stuff in virtualenv instead."; \
		exit 1; \
	else \
		pip install -r requirements/prod.txt; \
	fi

setup-dev:
	@if [ -z $$VIRTUAL_ENV ]; then \
		echo "Please set up virtualenv first."; \
		exit 1; \
	fi
	$(MAKE) requirements-dev
	$(MAKE) test
	[ ! -f $(PROJECT_NAME)/settings/local.py ] && \
		echo 'from .dev import *' > $(PROJECT_NAME)/settings/local.py
	python manage.py migrate
	echo "Now run: python manage.py runserver and visit http://localhost:8000/"

update:
	git pull
	$(MAKE) clean
	$(MAKE) requirements
	python manage.py migrate --noinput
	python manage.py collectstatic --noinput

deploy: update
	sudo service restart conference-web

lint:
	flake8 --exclude=.git,migrations --max-complexity=10 .

docker-check:
	@command -v docker >/dev/null 2>&1 || \
		{ echo >&2 "Docker needs to be installed and on your PATH.  Aborting."; exit 1; }

migrate:
	@docker exec -it `docker-compose ps -q web` python manage.py migrate

shell:
	@docker exec -it `docker-compose ps -q web` /bin/bash

run:
	@docker-compose up

db-prompt:
	@echo "Starting interactive database prompt (current dir mounted to /tmp/codebase)...";
	@docker exec -it `docker-compose ps -q db` psql -Upostgres

db-restore:
	@if [ ! -f webcampdb.sql ]; then \
		echo "Aborting! Can't find backup file. Database backup file must be named webcampdb.sql and located in the current directory!"; \
		exit 1; \
	fi
	@echo "Restoring database from backup file: webcampdb.sql"
	@cat webcampdb.sql | docker exec -i `docker-compose ps -q db` psql -Upostgres

superuser:
	@docker exec -it `docker-compose ps -q web` python manage.py createsuperuser

sync-media:
	rsync -rv webcamp:web/conference-web/project/media/uploads project/media/uploads
