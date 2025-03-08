from django.urls import path
from .views import (
    ProjectCreateView, ProjectListView, ProjectDetailView,
    ProjectUpdateView, ProjectDeleteView
)

urlpatterns = [
    path('proje_ekle/', ProjectCreateView.as_view(), name='proje-ekle'),
    path('projeler/', ProjectListView.as_view(), name='projeler'),
    path('projeler/<int:pk>/', ProjectDetailView.as_view(), name='proje-detay'),
    path('projeler/<int:pk>/update/', ProjectUpdateView.as_view(), name='proje-guncelle'),
    path('projeler/<int:pk>/delete/', ProjectDeleteView.as_view(), name='proje-sil'),
]
