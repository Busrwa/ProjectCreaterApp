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
    ProjectFileDeleteView,
    TaskCreateView,
    TaskListView,
    TaskDetailView,
    TaskUpdateView,
    TaskDeleteView
)

urlpatterns = [
    path('project-add/', ProjectCreateView.as_view(), name='project-add'), #sadece admin yapabilir.
    path('project/', ProjectListView.as_view(), name='projeler'), #herkes(admin harici) kendi team_lead ya da member olduğu projelerin listesini görür.
    path('project/<int:pk>/', ProjectDetailView.as_view(), name='proje-detay'), #endpointin permission'ı project/ endpointi gibi düzenlendi. Eğer belirtilen projeye teamlead ya da member olarak kayıtlıysa görebilir.
    path('project/<int:pk>/update/', ProjectUpdateView.as_view(), name='proje-guncelle'), #Sadece team_lead ve admin yapabilir.
    path('project/<int:pk>/delete/', ProjectDeleteView.as_view(), name='proje-sil'), #sadece admin yapabilir.

    # Dosya işlemleri için URL'ler
    path('project/<int:project_id>/file/upload/', ProjectFileUploadView.as_view(), name='file-upload'), #team-lead, member ve admin ekleme yapabilmeli.
    path('project/file/<int:pk>/download/', ProjectFileDownloadView.as_view(), name='file-download'),  #team-lead, member ve admin indirme yapabilmeli.
    path('project/file/<int:pk>/delete/', ProjectFileDeleteView.as_view(), name='file-delete'),  #team-lead ve admin silme yapabilmeli.

    # Task işlemleri
    path('task-add/', TaskCreateView.as_view(), name='task-add'),
    path('tasks/', TaskListView.as_view(), name='tasks'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/<int:pk>/update/', TaskUpdateView.as_view(), name='task-update'),
    path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),
]

# Geliştirme ortamında medya dosyalarını servis etme
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

