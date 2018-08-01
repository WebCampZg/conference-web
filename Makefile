PROJECT_NAME=project
MANAGE=python manage.py
SETTINGS=--settings=$(PROJECT_NAME).settings.test


.PHONY: test clean lint sync-media css css-watch

server:
	$(MANAGE) runserver

shell:
	$(MANAGE) shell_plus

test:
	pytest

clean:
	rm -rf .coverage cover
	find . -name '*.pyc' -exec rm '{}' ';'

lint:
	-@flake8 .

sync-media:
	rsync -av webcamp:web/conference-web/project/media/ project/media/

css:
	sassc --style compressed --sourcemap --load-path=. --load-path=node_modules/foundation-sites/scss ui/styles/style.scss ui/dist/styles/style.css

css-watch:
	make css
	@while true; do \
		inotifywait -qre close_write ui/styles; make css; \
	done
