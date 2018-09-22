"""vraagdepolitiek URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from graphene_django.views import GraphQLView
from backend.views import QuestionList, QuestionDetail, QuestionCreate, QuestionUpdate, QuestionDelete, QuestionUpvote

urlpatterns = [
    path('q/', QuestionList.as_view(), name='questions'),
    path('q/<int:pk>/', QuestionDetail.as_view(), name='question-detail'),
    path('q/create/', QuestionCreate.as_view(), name='question-create'),
    path('q/<int:pk>/edit/', QuestionUpdate.as_view(), name='question-update'),
    path('q/<int:pk>/delete/', QuestionDelete.as_view(), name='question-delete'),
    path('q/<int:pk>/upvote/', QuestionUpvote.as_view(), name='question-upvote'),

    # API Graphql endpoint
    re_path(r'^api/graphql', GraphQLView.as_view(graphiql=True)),
    path('admin/', admin.site.urls),

    # Route everything that doesn't match the other paths to frontend
    re_path(r'^', TemplateView.as_view(template_name='index.html')),
]
