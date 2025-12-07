from django.contrib import admin
from .models import ResumeTemplate, UserResume

@admin.register(ResumeTemplate)
class ResumeTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'template_type', 'is_active', 'created_at']
    list_filter = ['template_type', 'is_active']
    search_fields = ['name', 'description']

@admin.register(UserResume)
class UserResumeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'template', 'created_at']
    list_filter = ['template', 'created_at']
    search_fields = ['user__username', 'template__name']
