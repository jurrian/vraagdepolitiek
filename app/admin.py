from django.contrib import admin
from .models import User, Question, Answer, Theme
from django.contrib.auth.admin import UserAdmin

admin.site.register(User, UserAdmin)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Theme)
