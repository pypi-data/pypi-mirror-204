from django.contrib import admin

from .models import ProjectConsent, ProjectConsentCategory, ProjectConsentFile, ProjectConsentToken


class ProjectConsentTokenAdmin(admin.ModelAdmin):
    list_display = 'id', 'project', 'subject', 'created_at'


admin.site.register(ProjectConsent)
admin.site.register(ProjectConsentCategory)
admin.site.register(ProjectConsentFile)
admin.site.register(ProjectConsentToken, ProjectConsentTokenAdmin)
