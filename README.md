# django-openid-auth

# INSTALLATION
## Setup Virtual Environment
``` Bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Create Django Project
``` Bash
django-admin startproject django_openid_auth
```

## Create Django App
``` Bash
cd django_openid_auth
python manage.py startapp auth
```

## Connecting to PSQL Database
``` Bash
cat setup_dev_db.sql | psql -U postgres -h localhost -p 5432
psql "postgres://test_dev:test_dev_pwd@localhost:5432/testing_db"
```

## Add Pre-Commit Hooks
``` Bash
# Make sure you have setup.cfg and .pre-commit-config.yaml in the root directory
pre-commit install
```

# TESTING
``` Bash
# Coverage test
cd django_openid_auth/
coverage run manage.py test
coverage html
# or
coverage report

# bandit test
bandit --recursive django_openid_auth

# Django tests
python manage.py test
```

## Running the Server
``` bash
python manage.py migrate
python manage.py runserver
```
