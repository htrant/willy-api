# Willy-API

Attempt to build Web APIs with [Django](https://www.djangoproject.com) and [REST framework](http://www.django-rest-framework.org), which are required to run the project.


## Installation
##### Install [virtualenv](https://virtualenv.pypa.io/en/latest/index.html)
```
$ pip install virtualenv
$ virtualenv ENV
```
##### Dependencies (Django, REST framework included)
```
$ cd server/willy
$ pip install -r requirements.txt
```


## Database
### Setup
Change database setting at `base/settings.py`

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',		# your schema name
        'USER': '',		# your user
        'PASSWORD': '',	# your password
    }
}
```

Install [mysql-connector-python](https://dev.mysql.com/downloads/connector/python/2.1.html) (if needed)

```
$ pip install mysql-python
```


### Create and run migration
```
$ python manage.py makemigrations blog
$ python manage.py migrate
```


## Start server

Run server at port 88

```
$ python manage.py runserver 88
```


## Account APIs

### Register new account
Sample request (`password` is md5-hased)

```
POST /api/blog/account/register HTTP/1.1
Host: 127.0.0.1:88
Content-Type: application/json
Cache-Control: no-cache

{
    "email" : "contact@test.com",
    "password" : "b8085a89f6f056c410093b22c86ee8b6",
    "first_name" : "Contact",
    "last_name" : "Test Company"
}
```

Sample response

```
{
  "message": "The request is successfully executed",
  "code": 0,
  "data": {
    "id": 7,
    "name": "Contact Test Company",
    "email": "contact@test.com"
  },
  "success": true
}
```

### Verify account
Sample request

```
POST /api/blog/account/verify HTTP/1.1
Host: 127.0.0.1:88
Content-Type: application/json
Cache-Control: no-cache

{
    "token": "df9b7dcfe2c341e195db722c7d667bfb"
}
```

Sample response

```
{
  "message": "The request is successfully executed",
  "code": 0,
  "data": {
    "email": "contact@test.com",
    "username": "",
    "first_name": "Contact",
    "last_name": "Test Company",
    "phone": "",
    "created_date": "2015-11-12T13:45:30.035203",
    "updated_date": "2015-11-12T13:47:25.119224",
    "active_flg": 1,
    "id": 7,
    "token": "32571638bab24b7787c171ff77df7e1a",
    "expired": "2015-12-12T13:47:25.119224"
  },
  "success": true
}
```