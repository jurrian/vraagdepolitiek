from rest_framework import serializers
from app.models.publication import Question


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        # fields = ('id', 'title', 'code', 'linenos', 'language', 'style')
        fields = '__all__'
