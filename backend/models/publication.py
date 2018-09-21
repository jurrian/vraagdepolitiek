from django.conf import settings
from django.db import models
from django.urls import reverse


class Publication(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    summary = models.CharField(max_length=260)  # 280
    full_text = models.TextField()
    publication_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.summary


class Question(Publication):
    answers = models.ManyToManyField('Answer', blank=True, through='QuestionAnswer')
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


class QuestionAnswer(models.Model):
    question = models.ForeignKey('Question', on_delete=models.PROTECT)
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE)


class Theme(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
