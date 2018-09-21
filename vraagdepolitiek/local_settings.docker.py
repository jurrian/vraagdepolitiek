# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/
SECRET_KEY = 'develop'

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'vraagdepolitiek',
        'USER': 'vraagdepolitiek',
        'PASSWORD': 'vraagdepolitiek',
        'HOST': 'db',
        'PORT': '3306',
    }
}
