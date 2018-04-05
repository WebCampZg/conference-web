# Webcamp Zagreb conference web

[![Travis](https://img.shields.io/travis/WebCampZg/conference-web.svg?style=flat-square)]()

This repo holds the source code for [webcampzg.org](http://webcampzg.org/).

## Prerequisites

* build essentials (gcc and friends)
* git
* python3 + python3-dev
* fabric
* virtualenv
* virtualenvwrapper
* postgresql 9.6+
* libjpeg, libtiff (for Pillow)
* [yarn](https://yarnpkg.com/lang/en/docs/install/)

On Debian or Ubuntu:

Add the yarn repo:

```
curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
```

Install packages:

```
sudo apt install build-essential git python3 python3-dev fabric virtualenv virtualenvwrapper postgresql libjpeg-dev libtiff5-dev yarn nodejs-legacy sassc
```

Note: `nodejs-legacy` just provides a `/usr/bin/node` symlink to
`/usr/bin/nodejs` which yarn requires.

## Clone the project

```
git@github.com:WebCampZg/conference-web.git
cd conference-web
```

## Database setup

Presuming you have a working postgresql database set up, and that your SSL key
is in `.ssh/authorized_keys` on production server.

If you don't have a database user (replace `<user>` with your username):
```
sudo -u postgres createuser --superuser --password <user>
```

The `refresh_db` fabric command will drop the local database `webcamp` if it
exists and import the production data:

```
fab refresh_db
```

See `fabfile.py` for details.

## Python setup

Create a new virtual env for the project:

```
mkvirtualenv --python=`which python3` conference-web
```

If you already have a virtualenv then just activate it:

```
workon conference-web
```

Install dependencies into the virutal env:

```
pip install -r requirements/dev.txt
```

Create a local settings file `project/settings/local.py` with the following minimal configuration:

```
from .base import *
import dj_database_url

DATABASES = {'default': dj_database_url.config(
    default='postgres://<user>:<pass>@localhost:5432/webcamp'
)}
```

Add a random SECRET_KEY to the configuration file. Here's a oneliner:

```
python -c "import random,string;print('\nSECRET_KEY=\"{}\"\n'.format(''.join([random.SystemRandom().choice(string.ascii_letters) for i in range(63)])))" >> project/settings/local.py
```

You can now run the Django server:

```
./manage.py runserver
```

## Sync media

If you wish, copy the media files (e.g. user images and uploads) from the server:

```
make sync-media
```

## Build CSS

CSS is built from source SCSS files in `ui/styles` using [sassc](https://github.com/sass/sassc), and stored in `ui/dist/styles`. The generated CSS should be committed to the repo.

Install prerequisites ([Zurb Foundation](https://foundation.zurb.com/sites/docs/)):
```
yarn install
```

Now you can compile the styles:
```
make css
```

To watch for changes and automatically rebuild css:
```
make css-watch
```

## Deploy

To deploy the changes, first commit, merge and push your changes to `master`
branch, then run:

```
fab deploy
```

Requires your SSH key on the server.
