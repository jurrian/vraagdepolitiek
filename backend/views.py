from django.contrib.auth import login
from django.contrib.auth.views import PasswordResetConfirmView
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from backend.models.publication import Question


class QuestionList(ListView):
    model = Question


class QuestionDetail(DetailView):
    model = Question


class QuestionCreate(CreateView):
    model = Question
    fields = ['summary', 'full_text', 'themes']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class QuestionUpdate(UpdateView):
    model = Question
    fields = ['summary', 'full_text', 'themes']


class QuestionDelete(DeleteView):
    model = Question
    success_url = reverse_lazy('questions')

    def delete(self, request, *args, **kwargs):
        question = self.get_object()
        if question.is_user_deletable():
            return super().delete(request, *args, **kwargs)
        return HttpResponseForbidden("Can't delete a question that has answers")


class QuestionUpvote(SingleObjectMixin, View):
    model = Question

    def get(self, request, pk):
        question = self.get_object()

        try:
            question.user_support.add(self.request.user)
        except TypeError:
            return HttpResponseBadRequest('Invalid user id: {}'.format(self.request.user))

        return HttpResponse('Success')


class UserCreationConfirmView(TemplateView, PasswordResetConfirmView):
    post_reset_login = True
    post_reset_login_backend = None
    success_url = None
    template_name = 'registration/user_creation_complete.html'
    title = _('User confirmation completed')

    def get(self, *args, **kwargs):
        if self.validlink:
            self.user.is_active = True
            self.user.save()

            if self.post_reset_login:
                login(self.request, self.user, self.post_reset_login_backend)

        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.validlink:
            context['validlink'] = True
        else:
            context.update({
                'title': _('User confirmation unsuccessful'),
                'validlink': False,
            })
        return context
