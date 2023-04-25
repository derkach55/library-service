# DRF Library Api

Api service for managing books and book borrowings

# Installing using GitHub

```
git clone https://github.com/derkach55/library-service.git
cd library-service
python -m venv venv
source venv/bin/activate (on Linux)
venv\Scripts\activate (on Windows)
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 
docker run -d -p 6379:6379 redis
celery -A library_service worker -l INFO
celery -A library_service beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
```
Don`t forget add ```.env``` file

## Getting access

* create user via /api/user/register/
* get access token via /api/user/token/

## Features

* JWT authentication
* Admin panel
* Documentation at api/schema/swagger-ui/
* Managing books and borrowings
* Creating books, borrowings
* Filtering borrowings
* Telegram notifications
* Stripe payments