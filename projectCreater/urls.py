from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('your_app_name.urls')),  # Auth işlemleri için uygulamanızın URLsini dahil edin
    path('projeler/', include('projeler_app_name.urls')),  # Projeler sayfası için URL'yi dahil edin
]
