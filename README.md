# Python 3.11.0 > Django v3.2

A short description of your project goes here. Explain what it does and why it’s useful.

---

## 🛠️ Tech Stack

- **Language**: Python 3.11.0
- **Framework**: Django 3.2
- **API**: Django REST Framework

---

## 📝 Notes

- Environment variables should be configured inside a .env file (handled by python-decouple).

## 📦 Requirements

Install the following dependencies:

```js
python3.11 -m venv .venv || py -3.11 -m venv .venv
```

```js

asgiref==3.9.2
Django==3.2
djangorestframework==3.14.0
djongo==1.3.6
dnspython==2.8.0
pymongo==3.12.3
python-decouple==3.8
pytz==2025.2
sqlparse==0.2.4
tzdata==2025.2

```

```js
pip install -r requirements.txt || pip freeze > requirements.txt
```

DB Setup also add Djongo schema.

```js
DJONGO = {
    'SCHEMA': {
        'USER': {
            'ID_TYPE': 'int',  # Force integer IDs for User model
        }
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': config('MONGO_NAME'),
        'CLIENT': {
            'host': config('MONGO_URI'),
        }
    }
}

```

```js
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

```

# 📂 Project Structure

```js
your-repo/
│── manage.py
│── your_app/
│── .gitignore
│── requirements.txt
│── README.md
```
