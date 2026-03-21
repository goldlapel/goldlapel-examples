SECRET_KEY = "dev-only-not-secret"

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "todos",
]

MIDDLEWARE = []

ROOT_URLCONF = "todoapp.urls"

DATABASES = {
    "default": {
        "ENGINE": "django_goldlapel",
        "NAME": "todos",
        "USER": "gl",
        "PASSWORD": "gl",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
