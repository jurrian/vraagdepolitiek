from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.safestring import mark_safe

from backend.managers import UserManager


class Profile(models.Model):
    picture = models.ImageField(blank=True, null=True, max_length=200, upload_to='')
    gender = models.SmallIntegerField(blank=True, null=True, choices=((0, 'Man'), (1, 'Vrouw')))
    birth_date = models.DateField(blank=True, null=True)

    class Meta:
        abstract = True

    def image_tag(self):
        return mark_safe('<img src="%s" width=100 height=100 />' % self.picture)
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True


class User(AbstractUser, Profile):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # removes email from REQUIRED_FIELDS

    email = models.EmailField(unique=True)  # changes email to unique and blank to false

    objects = UserManager()


class Representative(Profile):
    user = models.OneToOneField('User', blank=True, null=True, on_delete=models.SET_NULL)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150, blank=True)
    organization = models.ManyToManyField('Organization', blank=True)
    # role = models. through?
    email = models.EmailField(blank=True)
    twitter = models.CharField(max_length=16, blank=True)

    # themes coupled through assignments

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def get_organization(self):
        return ", ".join([x.name for x in self.organization.all()])

    def __str__(self):
        return self.get_full_name()


class Organization(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
