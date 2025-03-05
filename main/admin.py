from django.contrib import admin
from .models import Application


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'resume_file_link', 'created_at')
    list_filter = ('user', 'full_name')
    search_fields = ('user', 'full_name')
    readonly_fields = ('resume_file_link', )
    list_per_page = 50


admin.site.register(Application, ApplicationAdmin)