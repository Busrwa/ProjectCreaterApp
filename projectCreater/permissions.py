from rest_framework import permissions
from .models import Project  # Eğer Project modeliniz farklı bir uygulamadaysa yolu ayarlayın

class IsTeamLeadOrAdmin(permissions.BasePermission):
    """
    Sadece takım lideri veya admin kullanıcıların erişimine izin verir.
    """
    def has_object_permission(self, request, view, obj):
        # Güvenli metotlara (GET, HEAD, OPTIONS) her zaman izin verilir.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Obje seviyesinde izin kontrolü:
        # Kullanıcı admin ise veya objenin takım lideri ise izin verilir.

        return request.user.is_superuser or obj.team_lead == request.user


class CanListProjects(permissions.BasePermission):
    """
    Sadece takım lideri veya admin rolündeki kullanıcıların projeleri listelemesine izin verir.
    """
    def has_permission(self, request, view):
        # Sadece GET istekleri (listeleme) için kontrol yapıyoruz.
        if request.method == 'GET':
            return request.user.is_authenticated and (request.user.is_superuser or hasattr(request.user, 'role') and request.user.role == 'team_lead')
        return True  # Diğer metotlara (POST vb.) izin vermek için (gerekirse düzenlenebilir)