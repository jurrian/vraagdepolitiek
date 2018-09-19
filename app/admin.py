from django.contrib import admin
from app.models.profile import User, Representative, Organization
from app.models.publication import Question, Answer, QuestionAnswer, Theme
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        (_('Personal info'), {'fields': ('picture', 'first_name', 'last_name', 'gender', 'birth_date')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_active', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'first_name', 'last_name', 'username')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)


class AnswerInline(admin.TabularInline):
    model = QuestionAnswer
    readonly_fields = ['answer']
    extra = 0


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]


admin.site.register(Answer)
admin.site.register(QuestionAnswer)
admin.site.register(Theme)
admin.site.register(Representative)
admin.site.register(Organization)
