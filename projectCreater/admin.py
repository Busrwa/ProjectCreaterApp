# 02.04.2025 tüm hatalar bakıldı
from django.contrib import admin
from .models import Project, ProjectFile

admin.site.register(Project)
admin.site.register(ProjectFile)
