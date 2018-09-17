"""vragenvuur URL Configuration

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
from app.views import QuestionList, QuestionDetail, QuestionCreate, QuestionUpdate, QuestionDelete, QuestionUpvote
from django.urls import path

urlpatterns = [
    path('q/', QuestionList.as_view(), name='questions'),
    path('q/detail/<int:pk>/', QuestionDetail.as_view(), name='question-detail'),
    path('q/create/', QuestionCreate.as_view(), name='question-create'),
    path('q/edit/<int:pk>/', QuestionUpdate.as_view(), name='question-update'),
    path('q/delete/<int:pk>/', QuestionDelete.as_view(), name='question-delete'),
    path('q/upvote/<int:pk>/', QuestionUpvote.as_view(), name='question-upvote'),
    path('admin/', admin.site.urls),
]
