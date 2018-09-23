from django.conf import settings
from django.db import models
from django.urls import reverse


class Publication(models.Model):
    summary = models.CharField(max_length=260)  # 280
    full_text = models.TextField()
    publication_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.summary


class Question(Publication):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL,
                             help_text='The user that posted the question.')
    organization = models.ForeignKey('Organization', on_delete=models.PROTECT,
                                     help_text='The legislative body or municipality in which this question is posted.')
    requests = models.TextField(blank=True, help_text='What the user asks from the Representatives.')
    answers = models.ManyToManyField('Answer', blank=True, through='QuestionAnswer')
    themes = models.ManyToManyField('Theme', blank=True)
    user_support = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='user_support_set', blank=True,
                                          help_text='The users that upvoted this question.')
    fb_support_count = models.PositiveSmallIntegerField(blank=True, default=0)
    twitter_support_count = models.PositiveSmallIntegerField(blank=True, default=0)

    def get_absolute_url(self):
        return reverse('question-detail', kwargs={'pk': self.pk})

    def is_user_deletable(self):
        if self.answers.count() > 0:
            return False
        return True

    @property
    def user_support_count(self):
        return self.user_support.count()

    @property
    def total_support_count(self):
        return self.user_support_count + self.fb_support_count + self.twitter_support_count


class Answer(Publication):
    user = models.ForeignKey('Representative', null=True, on_delete=models.SET_NULL,
                             help_text='The Representative that posted the answer.')
    efforts = models.TextField(blank=True, help_text='The effort that Representative has done already.')
    pledges = models.TextField(blank=True, help_text='What the Representative promises to do.')


class QuestionAnswer(models.Model):
    question = models.ForeignKey('Question', on_delete=models.PROTECT)
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE)

    @property
    def author(self):
        return self.answer.user


class Theme(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
