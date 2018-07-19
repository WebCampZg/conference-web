from fabric.api import run, cd, env, local

env.hosts = ['webcampzg.org']
env.user = 'webcamp'

PROJECT_HOME = '/home/webcamp/web/conference-web'
DUMP_FILE = "/tmp/conference-web-$(date +%Y-%m-%d).sql"
REMOTE_BIN = "/home/webcamp/.virtualenvs/conference-web/bin/"


def deploy():
    with cd(PROJECT_HOME):
        run("git pull")
        run(REMOTE_BIN + "pip install -r requirements/prod.txt")
        run(REMOTE_BIN + "python manage.py migrate")
        run(REMOTE_BIN + "python manage.py collectstatic --no-input")
        run("sudo service conference-web reload")


def upgrade():
    with cd(PROJECT_HOME):
        run(REMOTE_BIN + "pip install -U -r requirements/prod.txt")


def backup_db():
    # Make dump on host
    run("rm -f {}".format(DUMP_FILE))
    run("pg_dump -d webcamp --no-owner > {}".format(DUMP_FILE))

    # Fetch dump
    local("scp webcamp:{0} .".format(DUMP_FILE))

    # Cleanup
    run("rm -f {}".format(DUMP_FILE))


def refresh_db():
    # Make dump on host and fetch it
    run("rm -f {}".format(DUMP_FILE))
    run("pg_dump -d webcamp --no-owner > {}".format(DUMP_FILE))
    run("gzip {}".format(DUMP_FILE))
    local("scp webcamp:{0}.gz {0}.gz".format(DUMP_FILE))
    local("gunzip {0}.gz".format(DUMP_FILE))

    # Recreate the database locally
    local("dropdb --if-exists webcamp")
    local("createdb webcamp")
    local("psql -d webcamp < {}".format(DUMP_FILE))

    # Cleanup
    run("rm -f {}".format(DUMP_FILE))
    local("rm -f {}".format(DUMP_FILE))
