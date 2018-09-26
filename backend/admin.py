from django.contrib import admin
from django.contrib import messages
from django.contrib.admin.models import LogEntry
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.urls import path
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from backend.models.profile import User, Representative, Organization
from backend.models.publication import Question, Answer, QuestionAnswer, Theme


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
    readonly_fields = ['author']
    extra = 0


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('summary', 'user', 'organization', 'total_support_count', 'publication_datetime', 'published',)
    ordering = ('-publication_datetime',)
    date_hierarchy = 'publication_datetime'
    list_filter = ('publication_datetime', 'published',)
    list_display_links = ('summary', 'published',)
    search_fields = ('summary', 'full_text',)
    show_full_result_count = True

    exclude = ('published',)
    readonly_fields = ('fb_support_count', 'twitter_support_count',)
    filter_horizontal = ('user_support', 'themes',)
    inlines = [AnswerInline]

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """Add show_publish to context when rendering admin/submit_line.html"""
        question = Question.objects.get(pk=object_id)
        if not question.published:
            try:
                extra_context['show_publish'] = True
                extra_context['show_unpublish'] = False
            except TypeError:
                extra_context = {
                    'show_publish': True,
                    'show_unpublish': False,
                }
        else:
            try:
                extra_context['show_publish'] = False
                extra_context['show_unpublish'] = True
            except TypeError:
                extra_context = {
                    'show_publish': False,
                    'show_unpublish': True,
                }
        return self.changeform_view(request, object_id, form_url, extra_context)

    def publish_question(self, request, object_id):
        if not request.user.has_perm('backend.publish_question'):
            raise PermissionDenied

        question = Question.objects.get(pk=object_id)
        question.published = True
        question.save()

        self.log_change(request, question, 'Published.')

        msg = _('%(name)s has been published.' % {'name': question})
        self.message_user(request, msg, messages.SUCCESS)

        return HttpResponseRedirect(reverse('admin:backend_question_changelist'))

    def unpublish_question(self, request, object_id):
        # Uses the same permissions publish_question for unpublishing
        if not request.user.has_perm('backend.publish_question'):
            raise PermissionDenied

        question = Question.objects.get(pk=object_id)
        question.published = False
        question.save()

        self.log_change(request, question, 'Unpublished.')

        msg = _('%(name)s has been unpublished.' % {'name': question})
        self.message_user(request, msg, messages.INFO)

        return HttpResponseRedirect(reverse('admin:backend_question_changelist'))

    def get_urls(self):
        """Add additional admin urls for (un)publishing."""
        urls = super().get_urls()
        urls.insert(0, path('<path:object_id>/publish/',
                            self.admin_site.admin_view(self.publish_question),
                            name='backend_question_publish'))
        urls.insert(1, path('<path:object_id>/unpublish/',
                            self.admin_site.admin_view(self.unpublish_question),
                            name='backend_question_unpublish'))
        return urls


@admin.register(Representative)
class RepresentativeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'twitter', 'email', 'get_organization')
    readonly_fields = ('image_tag',)


admin.site.register(Answer)
admin.site.register(Theme)
admin.site.register(Organization)
admin.site.register(LogEntry)
