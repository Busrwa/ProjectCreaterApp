from rest_framework import permissions
from rest_framework.permissions import BasePermission

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

class IsProjectMemberOrForbidden(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated  # Kullanıcı giriş yapmış mı?

    def has_object_permission(self, request, view, obj):
        # Admin her şeye erişebilir
        if request.user.is_superuser:
            return True
        # Kullanıcı takım lideri mi veya proje ekibinde mi?
        if request.user == obj.team_lead or request.user in obj.team_members.all():
            return True
        return False  # Aksi takdirde erişim izni yok

class CanUploadFileToProject(permissions.BasePermission):
    """
    Sadece admin, takım lideri veya proje üyesinin projeye dosya yüklemesine izin verir (CreateAPIView için).
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            project_id = view.kwargs.get('project_id')
            if project_id is None or not request.user.is_authenticated:
                return False
            try:
                project = Project.objects.get(pk=project_id)
                return request.user.is_superuser or project.team_lead == request.user or request.user in project.team_members.all()
            except Project.DoesNotExist:
                return False
        return True
