from django.contrib import admin
from .models import BotUser


class BotUserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'first_name', 'last_name', 'username', 'language_code', 'is_active', 'is_admin', 'created_at', 'updated_at')
    list_filter = ('is_active', 'is_admin', 'created_at', 'updated_at')
    search_fields = ('user_id', 'first_name', 'last_name', 'username')
    list_per_page = 50


admin.site.register(BotUser, BotUserAdmin)