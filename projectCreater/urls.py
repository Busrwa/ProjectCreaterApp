from django.urls import path
from .views import (
    ProjectCreateView, ProjectListView, ProjectDetailView,
    ProjectUpdateView, ProjectDeleteView
)

urlpatterns = [
    path('project-add/', ProjectCreateView.as_view(), name='proje-ekle'),
    path('project/', ProjectListView.as_view(), name='projeler'),
    path('project/<int:pk>/', ProjectDetailView.as_view(), name='proje-detay'),
    path('project/<int:pk>/update/', ProjectUpdateView.as_view(), name='proje-guncelle'),
    path('project/<int:pk>/delete/', ProjectDeleteView.as_view(), name='proje-sil'),
]
