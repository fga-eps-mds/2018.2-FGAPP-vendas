from order_microservice.settings.common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 't@8!=auy=1zf#_p0c-kttunhohb!rea=a3ckkhdupb#hei)dyu'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db', # set in docker-compose.yml
        'PORT': 5432 # default postgres port
    }
}

