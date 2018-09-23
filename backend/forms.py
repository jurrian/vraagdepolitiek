from django import forms
from backend.models.publication import Question
from graphql import GraphQLError


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['summary', 'full_text', 'themes', 'organization']

    def is_valid(self):
        if not super().is_valid():
            for field, errors in self._errors.items():
                for error in errors:
                    raise GraphQLError(error)
        return True
