from django.contrib import admin, messages
from .models import *
from django.utils.translation import ngettext


admin.site.register(User)


@admin.action(description='Set marked article to published')
class addArticle(admin.ModelAdmin):
    def upload(self, request, queryset):
        status = queryset.update(status='p')
        self.message_user(request, ngettext(
            '%d article was successfully marked as published.',
            '%d articles were successfully marked as published.',
            status
        ) % status, messages.SUCCESS)
    list_display = ['title', 'date', 'status']
    ordering = ['date']
    actions = [upload]


admin.site.register(Content, addArticle)
