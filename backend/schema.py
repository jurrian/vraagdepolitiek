import graphene
from graphene_django import DjangoObjectType
from graphene_django.forms.mutation import DjangoModelFormMutation
from graphql import GraphQLError

from backend.models.profile import User, Representative, Organization, Party
from backend.models.publication import Question, Answer, Theme
from django.contrib.sites.models import Site
from backend.forms import QuestionForm

class UserType(DjangoObjectType):
    password = None

    class Meta:
        model = User
        only_fields = ('id', 'last_login', 'username', 'first_name', 'last_name', 'is_active', 'date_joined', 'picture',
                       'gender', 'birth_date', 'email', 'representative', 'question_set', 'user_support_set')
        description = 'An user with a profile, used for authentication.'


class QuestionType(DjangoObjectType):
    user_support_count = graphene.Int(description='The calculated count of UserSupport upvotes.')
    total_support_count = graphene.Int(description='Total calculated count of user, facebook and twitter support.')

    class Meta:
        model = Question
        description = 'A question asked by an user.'


class AnswerType(DjangoObjectType):
    class Meta:
        model = Answer
        description = 'An answer from a representative on a question.'


class RepresentativeType(DjangoObjectType):
    class Meta:
        model = Representative
        description = 'The profile of a representative, which might be coupled to a user.'


class ThemeType(DjangoObjectType):
    class Meta:
        model = Theme
        description = 'A political subject associated with a question or representative.'


class OrganizationType(DjangoObjectType):
    class Meta:
        model = Organization
        description = 'A legislative body or municipality which is coupled (and thus only visible) to a certain site.'


class PartyType(DjangoObjectType):
    class Meta:
        model = Party
        description = 'A political party which has representatives as members.'


class SiteType(DjangoObjectType):
    class Meta:
        model = Site
        description = 'The website domain which a organization belongs to. Depending on the request\'s host this ' \
                      'determines which organizations, and in turn which questions, to show.'


# noinspection PyMethodMayBeStatic,PyUnusedLocal
class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    current_user = graphene.Field(UserType)
    user_questions = graphene.List(QuestionType)

    questions = graphene.List(QuestionType)
    answers = graphene.List(AnswerType)

    def resolve_users(self, info):
        return User.objects.all()

    def resolve_current_user(self, info):
        if not info.context.user.is_authenticated:
            raise GraphQLError('No user logged in')
        return User.objects.get(pk=info.context.user.id)

    def resolve_user_questions(self, info):
        if not info.context.user.is_authenticated:
            raise GraphQLError('No user logged in')
        return Question.objects.filter(user=info.context.user)

    def resolve_questions(self, info):
        return Question.objects.all()

    def resolve_answers(self, info):
        return Answer.objects.all()

    class Meta:
        description = 'GraphQL query endpoint for vraagdepolitiek.nl and vraagdegemeente.nl.'


class CreateQuestion(DjangoModelFormMutation):
    class Meta:
        form_class = QuestionForm


def login_required(func):
    def wrapper(self, info, *args, **kwargs):
        if not info.context.user.is_authenticated:
            raise GraphQLError('No user logged in')
        return func(self, info, *args, **kwargs)
    return wrapper


class QuestionUpvote(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    ok = graphene.Boolean()

    @login_required
    def mutate(self, info, id):
        try:
            question = Question.objects.get(pk=id)
            question.user_support.add(info.context.user.id)
        except (TypeError, Question.DoesNotExist):
            raise

        if question.total_support_count == question.min_required_support:
            # Do some action
            pass

        return QuestionUpvote(ok=True)


class Login(graphene.Mutation):
    class Arguments:
        email = graphene.String()
        password = graphene.String()

    ok = graphene.Boolean()

    def mutate(self, info, email, password):
        from django.contrib.auth import authenticate, login
        user = authenticate(info.context, email=email, password=password)
        if user is not None:
            login(info.context, user)
            return Login(ok=True)
        else:
            return Login(ok=False)


class Mutations(graphene.ObjectType):
    login = Login.Field()
    create_question = CreateQuestion.Field()
    question_upvote = QuestionUpvote.Field()


# noinspection PyTypeChecker
schema = graphene.Schema(query=Query, mutation=Mutations)
