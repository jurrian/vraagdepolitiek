from django.views.generic import ListView, DetailView
from app.models import Question
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.views import View
from django.views.generic.detail import SingleObjectMixin


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
