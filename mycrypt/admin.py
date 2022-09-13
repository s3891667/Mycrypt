from django.contrib import admin, messages
from .models import *
from django.utils.translation import ngettext
from django.contrib.auth import get_permission_codename


admin.site.register(User)


@admin.action(description='Published')
@admin.action(permissions=['upload'])
class addArticle(admin.ModelAdmin):
    def upload(self, modeladmin, request, queryset):
        status = queryset.update(status='p')
        self.message_user(request, ngettext(
            '%d article was successfully marked as published.',
            '%d articles were successfully marked as published.',
            status
        ) % status, messages.SUCCESS)

    list_article = ['title', 'date']
    ordering = ['date']
    actions = [upload]

    def has_publish_permission(self, request):
        """Does the user have the publish permission?"""
        opts = self.opts
        codename = get_permission_codename('upload', opts)
        return request.user.has_perm('%s.%s' % (opts.app_label, codename))


admin.site.register(Content, addArticle)
