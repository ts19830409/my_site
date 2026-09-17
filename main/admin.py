from django.contrib import admin
from .models import Project, Certificate, Message, Award


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'github_url')


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_archived')
    list_filter = ('is_archived',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    readonly_fields = ('name', 'email', 'text', 'created_at')

    def has_add_permission(self, request):
        return False


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ('title',)