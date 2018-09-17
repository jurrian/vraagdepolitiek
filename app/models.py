from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from app.managers import UserManager
from django.urls import reverse


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # removes email from REQUIRED_FIELDS

    email = models.EmailField(_('email address'), unique=True)  # changes email to unique and blank to false

    objects = UserManager()


class Publication(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    summary = models.CharField(max_length=260)  # 280
    full_text = models.TextField()
    publication_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.summary


class Question(Publication):
    answers = models.ManyToManyField('Answer', blank=True)
    themes = models.ManyToManyField('Theme', blank=True)
    user_support = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='support', blank=True)

    def get_absolute_url(self):
        return reverse('question-detail', kwargs={'pk': self.pk})

    def is_user_deletable(self):
        if self.answers.count() > 0:
            return False
        return True


class Answer(Publication):
    pass


class Theme(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
