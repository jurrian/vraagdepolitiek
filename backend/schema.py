import graphene
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.sites.models import Site
from graphene_django import DjangoObjectType
from graphene_django.forms.mutation import DjangoModelFormMutation
from graphql import GraphQLError

from backend.forms import QuestionForm, UserCreationForm
from backend.models.profile import User, Representative, Organization, Party
from backend.models.publication import Question, Answer, Theme


class UserType(DjangoObjectType):

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

    questions = graphene.List(QuestionType)
    site_questions = graphene.List(QuestionType, site=graphene.ID())
    answers = graphene.List(AnswerType)
    representatives = graphene.List(RepresentativeType)
    organizations = graphene.List(OrganizationType)
    parties = graphene.List(PartyType)
    sites = graphene.List(SiteType, id=graphene.ID())

    def resolve_users(self, info):
        return User.objects.all()

    def resolve_current_user(self, info):
        if not info.context.user.is_authenticated:
            raise GraphQLError('No user logged in')

        return User.objects.get(pk=info.context.user.id)

    def resolve_questions(self, info):
        return Question.objects.all()

    def resolve_answers(self, info):
        return Answer.objects.all()

    def resolve_representatives(self, info):
        return Representative.objects.all()

    def resolve_organizations(self, info):
        return Organization.objects.all()

    def resolve_parties(self, info):
        return Party.objects.all()

    def resolve_sites(self, info, id=None):
        return Site.objects.all()

    def resolve_site_questions(self, info, site=None):
        if not site:
            site = info.context.site

        return Question.objects.filter(organization__site=site)

    class Meta:
        description = 'GraphQL query endpoint for vraagdepolitiek.nl and vraagdegemeente.nl.'


class CreateQuestion(DjangoModelFormMutation):
    class Meta:
        form_class = QuestionForm
        exclude_fields = ('id',)


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
        user = authenticate(info.context, email=email, password=password)
        if user is not None:
            login(info.context, user)
            return Login(ok=True)
        else:
            return Login(ok=False)


class CreateUser(DjangoModelFormMutation):
    class Meta:
        form_class = UserCreationForm
        exclude_fields = ('id',)

    @classmethod
    def perform_mutate(cls, form, info):
        """Added request to save method."""
        obj = form.save(request=info.context)
        kwargs = {cls._meta.return_field_name: obj}
        return cls(errors=[], **kwargs)


class PasswordReset(DjangoModelFormMutation):
    class Meta:
        form_class = PasswordResetForm
        model = User

    @classmethod
    def perform_mutate(cls, form, info):
        """Added request to save method."""
        obj = form.save(request=info.context)
        kwargs = {cls._meta.return_field_name: obj}
        return cls(errors=[], **kwargs)


class Mutations(graphene.ObjectType):
    login = Login.Field()
    create_user = CreateUser.Field()
    password_reset = PasswordReset.Field()

    create_question = CreateQuestion.Field()
    question_upvote = QuestionUpvote.Field()


# noinspection PyTypeChecker
schema = graphene.Schema(query=Query, mutation=Mutations)
