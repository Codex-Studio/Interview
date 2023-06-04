from django.contrib import admin

from apps.questions.models import Question, Mailing

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