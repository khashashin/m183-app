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

## Login
If you have configured GitHub, GitLab or default admin user  
you can log in using those credentials.

For instance: email: admin@mail.ch; password: admin

![image](https://user-images.githubusercontent.com/17837758/170585482-faace7ff-a043-401a-b1a3-8886dac9d514.png)

![image](https://user-images.githubusercontent.com/17837758/170585770-c051f771-ee73-48f5-8296-61b054ce959e.png)

![image](https://user-images.githubusercontent.com/17837758/170585830-ea5d7870-e0d8-436c-bf02-3ff82d1f80b1.png)

![image](https://user-images.githubusercontent.com/17837758/170585609-278c7447-55d5-46ff-956b-f8a517162276.png)

![image](https://user-images.githubusercontent.com/17837758/170585694-839d2880-d4be-445d-a989-e324791115f8.png)

# Projekt Documentation

### Login
Login implemented using django-allauth package.  
Also there is OAuth2 support for GitHub, GitLab.  
By default, you can use the following credentials:  
    Email: admin@mail.ch  
    Password: admin

### Session Handling
Session handling used to check if user is logged in.  
"Browser Commandline Tool" is available only for authenticated users.

### Using System Commands
There are defined two Tables: Command and Option.  
Each command has multiple options.  
User input first validated using BLACKLIST (see linux/views.py BLACK_LIST_CHARACTERS).

Then it is validated using Command and Option entries in the Database.

You can add new Commands and Options just by adding them through the admin interface (more about this below).

Also there is implementation of usage limitation on both Client and Server side.  
You can run commands only each 7 seconds.

### Admin Interface
You can log in to the admin interface using the admin credentials.  
The admin interface is available at http://127.0.0.1:8080/admin/

### Logging
In logs/ directory you can find log files for each command.   
Each client has its own log files for input and output.

### Secure Password Storage
Passwords are validated by multiple criteria.  
1. Length of password is at least 8 characters.
2. Password contains at least one digit.
3. Password contains at least one lowercase letter.
4. Password contains at least one uppercase letter.
5. Password contains at least one special character.
6. Is not similar to the username or email.
7. Is not listed in publicly available password lists. (https://haveibeenpwned.com/)

Passwords are stored in the database using [PBKDF2](https://en.wikipedia.org/wiki/PBKDF2) algorithm with a SHA256 hash.  
(More about hashing passwords in Django: [How Django stores passwords](https://docs.djangoproject.com/en/4.0/topics/auth/passwords/#how-django-stores-passwords))

### TLS Encryption of Communication
TLS is not configured to use locally.  
However, this will be done on the Server side using Traefik Reverse Proxy which provides TLS encryption out of the box.

Since the Idea of this Project is to be able to run it on a Smartlearn,  
the local TLS configuration is not implemented.

### New User Registration
New users can be registered using the admin interface, registration form or OAuth2.

### GUI - "Jeder hat seinen eigenen Geschmack"
GUI is implemented using Bootstrap 5 components.

### REST API
Since there is only one endpoint needed, the API is implemented using JSON Response.  
Web Commandline Tool sends the data over HTTP POST by using javascript [fetch](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch) function.

### OAuth2 instead of LDAP
In this project you can set up OAuth2 for GitHub, GitLab.
The LDAP configuration for Gibb was not implemented.

### Docker
You can run this project on a Docker container using `docker-compose up -d`.

### Roles and Permissions
This Project uses the Django-Roles which is a simple role management system.
It allows you to assign users to different groups.
Admin users are special users and there is an attribute called `is_admin` in the User model.
