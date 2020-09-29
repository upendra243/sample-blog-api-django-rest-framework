## Getting Started

Before we start, we need this to be installed:
- [Python3](https://www.python.org/downloads/)

## Project Setup

Unzip code to your workspace
```
cd /absolute/path/blog
```
Make virtual environment with python3 and activate it:
```
virtualenv .env --python=python3
source .env/bin/activate
```
Install Django and DjangoRestFramework:
```
pip install -r requirements.txt
```
Now sync database and create database user:
```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```
Run all test cases
```
python manage.py test
```

Run your developent server
```
python manage.py runserver
```

## Test API's
Now test API using browser at [localhost](http://localhost:8000/) or
import postman collection `blog.postman_collection.json` on your machine.

## API DOCS
API docs generated using Swagger `/docs/` is url for docs.
