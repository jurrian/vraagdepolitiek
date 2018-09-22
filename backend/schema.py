from graphene_django import DjangoObjectType
import graphene
import backend.models.publication


class User(DjangoObjectType):
    class Meta:
        model = backend.models.User


class Question(DjangoObjectType):
    class Meta:
        model = backend.models.publication.Question


class Answer(DjangoObjectType):
    class Meta:
        model = backend.models.publication.Answer


class Query(graphene.ObjectType):
    users = graphene.List(User)
    questions = graphene.List(Question)
    answers = graphene.List(Answer)

    def resolve_users(self, info):
        return backend.models.User.objects.all()

    def resolve_questions(self, info):
        return backend.models.publication.Question.objects.all()

    def resolve_answers(self, info):
        return backend.models.publication.Answer.objects.all()


schema = graphene.Schema(query=Query)
