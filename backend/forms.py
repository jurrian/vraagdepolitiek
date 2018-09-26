from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _

from backend.models.profile import User
from backend.models.publication import Question
from django.conf import settings

UserModel = get_user_model()


def send_mail(subject_template_name, email_template_name,
              context, from_email, to_email, html_email_template_name=None):
    """
    Send a django.core.mail.EmailMultiAlternatives to `to_email`.
    """
    subject = loader.render_to_string(subject_template_name, context)
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    body = loader.render_to_string(email_template_name, context)

    # Todo also test for tuples etc.
    if not type(to_email) == list:
        to_email = [to_email]

    email_message = EmailMultiAlternatives(subject, body, from_email, to_email)
    if html_email_template_name is not None:
        html_email = loader.render_to_string(html_email_template_name, context)
        email_message.attach_alternative(html_email, 'text/html')

    email_message.send()


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['summary', 'full_text', 'themes', 'organization']

    def save(self, commit=True):
        question = super().save(commit)
        if question and not settings.DEBUG:
            context = {
                'question': self.instance,
            }
            moderators = UserModel._default_manager_.filter(groups__name='Moderator')
            if moderators:
                send_mail(
                    subject_template_name=None,
                    email_template_name='backend/question_moderation_email.html',
                    context=context,
                    from_email=None,
                    to_email=[moderator.email for moderator in moderators]
                )
        return question


class UserCreationForm(DjangoUserCreationForm):
    class Meta(DjangoUserCreationForm.Meta):
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'gender',
                  'birth_date', 'picture']

    @staticmethod
    def send_confirm_mail(user, email, domain_override=None,
                          subject_template_name='registration/user_creation_subject.txt',
                          email_template_name='registration/user_creation_email.html',
                          use_https=False, token_generator=default_token_generator,
                          from_email=None, request=None, html_email_template_name=None,
                          extra_email_context=None):

        if not domain_override:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override
        context = {
            'email': email,
            'domain': domain,
            'site_name': site_name,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            'user': user,
            'token': token_generator.make_token(user),
            'protocol': 'https' if use_https else 'http',
            **(extra_email_context or {}),
        }
        send_mail(
            subject_template_name, email_template_name, context, from_email,
            email, html_email_template_name=html_email_template_name,
        )

    def save(self, commit=True, request=None):
        """
        Overridden in order to set is_active to False and send a confirmation
        mail with a link to set it to True.
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = False
        if commit:
            user.save()

        email = self.cleaned_data["email"]
        self.send_confirm_mail(user, email, request=request)
        return user

    def validate_unique(self):
        """
        Overridden in order to resend a confirmation mail when the emailaddress
        already exists but is not active and hasn't been logged in to.
        """
        exclude = self._get_validation_exclusions()
        try:
            self.instance.validate_unique(exclude=exclude)
        except ValidationError as e:
            try:
                existing_user = self._meta.model._default_manager.get(
                    email=self.instance.email,
                    is_active=0,
                    last_login__isnull=True
                )
                if existing_user:
                    self.send_confirm_mail(existing_user, existing_user.email,
                                           request=None)
                    e = ValidationError(
                        _('The emailaddress {} already exists but has not yet '
                          'been confirmed. We have sent you a new confirmation '
                          'link.').format(self.instance.email)
                    )
            except self._meta.model.DoesNotExist:
                # If no matching user exists, just follow base method.
                pass

            self._update_errors(e)
