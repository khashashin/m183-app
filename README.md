# Starting Project Locally on your Computer

If you prefer to use Docker then jump right to the [Docker](#docker-compose) section.

## Requirements
python >= 3.9

## Installation Backend
Create virtualenv and activate it

```bash
python3 -m venv .venv
source venv/bin/activate
```

Install dependencies
```bash
pip install -e .
```
or if you want to install all dependencies (including dev dependencies)
```bash
pip install -e '.[dev]'
```

## Prepare .env file
```bash
touch .env
```

## Make sure you add following environment variables to .env file

```bash
# To generate environment safe secret key, you can use:
# python -c 'from django.utils.crypto import get_random_string; print(get_random_string(50, "abcdefghijklmnopqrstuvwxyz0123456789!%^*(-_)"))'
SECRET_KEY=<your secret key>
SITE_NAME=<your site name> # 127.0.0.1:8000
ALLOWED_HOSTS=<your site name> # 127.0.0.1:8000 site.com site2.com
DEBUG=True # Change to False if you want to run in production

ADMIN_USERNAME=<your admin username> # admin
ADMIN_EMAIL=<your admin email> # admin@mail.ch
ADMIN_PASSWORD=<your admin password> # admin
```

## Initialize Database
This will initialize admin user (using defaults if nothing is provided) and create database
```bash
python manage.py initialize
```

## If you want to be able to sign up using GitHub or GitLab, you need to add following settings to .env file
```bash
GITHUB_CLIENT_ID=<your github client id>
GITHUB_CLIENT_SECRET=<your github client secret>
GITLAB_CLIENT_ID=<your gitlab client id>
GITLAB_CLIENT_SECRET=<your gitlab client secret>
```

## Docker Compose
```bash
docker-compose up -d
```
Open your browser and go to http://127.0.0.1:8080

![image](https://user-images.githubusercontent.com/17837758/170585482-faace7ff-a043-401a-b1a3-8886dac9d514.png)

![image](https://user-images.githubusercontent.com/17837758/170585770-c051f771-ee73-48f5-8296-61b054ce959e.png)

![image](https://user-images.githubusercontent.com/17837758/170585830-ea5d7870-e0d8-436c-bf02-3ff82d1f80b1.png)

![image](https://user-images.githubusercontent.com/17837758/170585609-278c7447-55d5-46ff-956b-f8a517162276.png)

![image](https://user-images.githubusercontent.com/17837758/170585694-839d2880-d4be-445d-a989-e324791115f8.png)

