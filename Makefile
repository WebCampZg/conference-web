PROJECT_NAME=project
MANAGE=python manage.py
SETTINGS=--settings=$(PROJECT_NAME).settings.test


.PHONY: all test coverage clean requirements requirements-dev \
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
	-@flake8 .

sync-media:
	rsync -av webcamp:web/conference-web/project/media/ project/media/

css:
	node_modules/.bin/node-sass ui/styles/style.scss ui/dist/styles/style.css --include-path=node_modules/foundation-sites/scss --source-map=true

css-watch:
	node_modules/.bin/node-sass ui/styles/style.scss ui/dist/styles/style.css --include-path=node_modules/foundation-sites/scss --source-map=true --watch
