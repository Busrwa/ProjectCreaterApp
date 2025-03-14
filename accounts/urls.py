from django.urls import path
from .views import RegisterAPI, LoginAPI, ProjectCreaterRedirectView, UserListView,UserUpdateView, UserDeleteView
from knox import views as knox_views  # Knox kimlik doğrulama sistemi için çıkış işlemleri

# Uygulamanın URL tanımlamaları
urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),  # Kullanıcı kayıt işlemi için endpoint
    path('login/', LoginAPI.as_view(), name='login'),  # Kullanıcı giriş işlemi için endpoint
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),  # Kullanıcıyı çıkış yaptırmak için endpoint

    #path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),  # Tüm cihazlardan çıkış yapmak için endpoint. Şuanlık kullanım dışı (14.03.2025).
    path('users/', UserListView.as_view(), name='user-list'),  # Admin kullanıcısı için
    path('user/<int:pk>/update/', UserUpdateView.as_view(), name='user-update'),  # Admin kullanıcısı için
    path('user/<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),  # Admin kullanıcısı için
]
