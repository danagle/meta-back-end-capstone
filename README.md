# Back-End Developer Capstone Project
This is part of the [Meta Back-End Developer Professional Certificate](https://www.coursera.org/professional-certificates/meta-back-end-developer) on Coursera.

## Project Setup

Setup the virtual environment and install the required packages:
```bash
cd /path/to/the/project
pipenv install
```

Edit `my.env` and set the environment variables for the database connection:
```bash
DJANGO_DB_NAME = 'capstone_db'
DJANGO_DB_HOST = '127.0.0.1'
DJANGO_DB_PORT = '3306'
DJANGO_DB_USER = 'root'
DJANGO_DB_PASSWORD = 'password'
```

Create and apply the migrations:
```bash
cd LittleLemon

python3 manage.py makemigrations

python3 manage.py migrate
```

Run the tests:
```bash
python3 manage.py test
```

Ready to launch:
```bash
python3 manage.py runserver
```

## Extras
The `sample_code.py` demonstrates the use of the following API endpoints:
 - /auth/users
 - /auth/users/me/
 - /auth/token/login/
 - /restaurant/menu/
 - /restaurant/booking/tables/

To run:
```bash
python3 sample_code.py
```
