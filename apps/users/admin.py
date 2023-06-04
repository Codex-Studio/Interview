from django.contrib import admin

from apps.users.models import TelegramUser

# Register your models here.
@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'date_joined', 'code')
    search_fields = ('username', 'first_name', 'last_name', 'date_joined', 'code')
    list_per_page = 20