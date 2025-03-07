from django.urls import path
from .views import RegisterAPI, LoginAPI, ProjectCreaterRedirectView
from knox import views as knox_views  # Knox kimlik doğrulama sistemi için çıkış işlemleri

# Uygulamanın URL tanımlamaları
urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),  # Kullanıcı kayıt işlemi için endpoint
    path('login/', LoginAPI.as_view(), name='login'),  # Kullanıcı giriş işlemi için endpoint
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),  # Kullanıcıyı çıkış yaptırmak için endpoint
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),  # Tüm cihazlardan çıkış yapmak için endpoint
]

