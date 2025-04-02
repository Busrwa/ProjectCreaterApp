# urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (
    ProjectCreateView,
    ProjectListView,
    ProjectDetailView,
    ProjectUpdateView,
    ProjectDeleteView,
    ProjectFileUploadView,
    ProjectFileDownloadView,
    ProjectFileDeleteView
)

urlpatterns = [
    path('project-add/', ProjectCreateView.as_view(), name='project-add'),
    path('project/', ProjectListView.as_view(), name='projeler'),
    path('project/<int:pk>/', ProjectDetailView.as_view(), name='proje-detay'),
    path('project/<int:pk>/update/', ProjectUpdateView.as_view(), name='proje-guncelle'),
    path('project/<int:pk>/delete/', ProjectDeleteView.as_view(), name='proje-sil'),

    # Dosya işlemleri için URL'ler
    path('project/<int:project_id>/file/upload/', ProjectFileUploadView.as_view(), name='file-upload'),
    path('project/file/<int:pk>/download/', ProjectFileDownloadView.as_view(), name='file-download'),
    path('project/file/<int:pk>/delete/', ProjectFileDeleteView.as_view(), name='file-delete'),
]

# Geliştirme ortamında medya dosyalarını servis etme
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
