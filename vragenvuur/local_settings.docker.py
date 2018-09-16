# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/
SECRET_KEY = 'develop'

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'vragenvuur',
        'USER': 'vragenvuur',
        'PASSWORD': 'vragenvuur',
        'HOST': 'db',
        'PORT': '3306',
    }
}
