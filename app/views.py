from django.views.generic import ListView
from app.models import Question


class QuestionList(ListView):
    model = Question
