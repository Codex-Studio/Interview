from typing import Any
from django.contrib import admin
import asyncio

from apps.questions.models import Question, Mailing
from apps.users.views import send_mailing

# Register your models here.
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'point')
    search_fields = ('user__username', 'title', 'point')
    list_per_page = 20

@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('title', 'mailing_type')
    list_per_page = 20

    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        asyncio.run(send_mailing(obj.user, obj.title, obj.mailing_type))
        return super().save_model(request, obj, form, change)