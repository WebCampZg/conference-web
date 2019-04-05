PROJECT_NAME=project
MANAGE=python manage.py
SETTINGS=--settings=$(PROJECT_NAME).settings.test

PLEX_VERSION=1.3.1
FOUNDATION_VERSION=6.3.1


.PHONY: test clean lint sync-media css css-watch

server:
	$(MANAGE) runserver

shell:
	$(MANAGE) shell_plus

test:
	pytest

clean:
	rm -rf .coverage cover sources
	find . -name '*.pyc' -exec rm '{}' ';'

lint:
	-@flake8 .

sync-media:
	rsync -av webcamp:web/conference-web/project/media/ project/media/

# Download IBM Plex and Foundation site sources
sources:
	curl https://github.com/IBM/plex/releases/download/v$(PLEX_VERSION)/Web.zip \
		-o sources/tmp/plex.zip --location --create-dirs
	curl https://github.com/zurb/foundation/archive/$(FOUNDATION_VERSION).zip \
		-o sources/tmp/foundation.zip --location --create-dirs
	unzip sources/tmp/plex.zip -d sources/tmp/plex/
	unzip sources/tmp/foundation.zip -d sources/tmp/foundation/
	mv sources/tmp/plex/Web sources/plex
	mv sources/tmp/foundation/foundation-sites-$(FOUNDATION_VERSION) sources/foundation
	rm -r sources/tmp

dist:
	rm -rf ui/dist/fonts/IBM-Plex-Mono/fonts/split
	mkdir -p ui/dist/fonts/IBM-Plex-Mono/fonts
	cp -r sources/plex/IBM-Plex-Mono/fonts/split \
		ui/dist/fonts/IBM-Plex-Mono/fonts/split

css:
	sassc \
		--sourcemap \
		--style compressed \
		--load-path=. \
		--load-path=sources/plex/scss/ \
		--load-path=sources/foundation/scss \
		ui/styles/style.scss \
		ui/dist/styles/style.css

css-watch:
	make css
	@while true; do \
		inotifywait -qre close_write ui/styles; make css; \
	done
