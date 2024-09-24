# django-telegram-bot

## Features

Built-in Telegram bot methods:
* `/broadcast` — send message to all users (admin command)
* `/export_users` — bot sends you info about your users in .csv file (admin command)
* `/stats` — show basic bot stats 

# How to run

## Quickstart: Polling & SQLite

The fastest way to run the bot is to run it in polling mode. This should be enough for quickstart:

Create `.env` file in root directory and copy-paste from `.env_example`,
don't forget to change telegram token.

Run migrations to setup database:
``` bash
python manage.py migrate
```

Create superuser to get access to admin panel:
``` bash
python manage.py createsuperuser
```

Run bot in polling mode:
``` bash
python run_polling.py 
```

If you want to open Django admin panel which will be located on http://localhost:8000/tgadmin/:
``` bash
python manage.py runserver
```

## Run locally using docker-compose
If you want just to run all the things locally, you can use Docker-compose which will start all containers for you.


### Docker-compose
To run all services (Django, Postgres) at once:
``` bash
docker-compose up -d --build
```

Try visit <a href="http://0.0.0.0:8000/tgadmin">Django-admin panel</a>.
