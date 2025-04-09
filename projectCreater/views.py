from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Project
from .serializers import ProjectSerializer
from rest_framework.permissions import IsAdminUser
from .permissions import IsTeamLeadOrAdmin, CanListProjects, IsProjectMemberOrForbidden
from django.db.models import Q  # Q nesnesini doğrudan import edelim
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Project, ProjectFile
from .serializers import ProjectSerializer, ProjectFileSerializer
from .permissions import IsTeamLeadOrAdmin
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Project, ProjectFile
from .serializers import ProjectFileSerializer
from .permissions import IsTeamLeadOrAdmin
from .permissions import CanUploadFileToProject
from rest_framework.exceptions import PermissionDenied


from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Task
from .serializers import TaskSerializer
from .permissions import IsTeamLeadOrAdmin, IsProjectMemberOrForbidden

from .models import Task
from .serializers import TaskSerializer

# Proje ekleme
class ProjectCreateView(generics.CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAdminUser]

# Tüm projeleri listeleme
class ProjectListView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Kullanıcının team_member olduğu veya team_lead olduğu projeleri filtrele
        return Project.objects.filter(
            Q(team_members=user) | Q(team_lead=user)
        ).distinct()
# Belirli bir projeyi görüntüleme
class ProjectDetailView(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsProjectMemberOrForbidden]
# Proje güncelleme
class ProjectUpdateView(generics.UpdateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsTeamLeadOrAdmin]

# Proje silme
class ProjectDeleteView(generics.DestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAdminUser]

# Proje dosyasını yüklemek için view
class ProjectFileUploadView(generics.CreateAPIView):
    queryset = ProjectFile.objects.all()
    serializer_class = ProjectFileSerializer
    permission_classes = [IsAuthenticated, CanUploadFileToProject]

    def perform_create(self, serializer):
        project_id = self.kwargs.get('project_id')
        project = get_object_or_404(Project, id=project_id)
        serializer.save(uploaded_by=self.request.user, project=project)


# Proje dosyasını indirmek için view
class ProjectFileDownloadView(generics.RetrieveAPIView):
    queryset = ProjectFile.objects.all()
    serializer_class = ProjectFileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        file_obj = self.get_object()
        return FileResponse(file_obj.file, as_attachment=True)

# Proje dosyasını silmek için view
class ProjectFileDeleteView(generics.DestroyAPIView):
    queryset = ProjectFile.objects.all()
    serializer_class = ProjectFileSerializer
    permission_classes = [IsAuthenticated, IsTeamLeadOrAdmin]

    def check_object_permissions(self, request, obj):
        # Eğer obje ProjectFile ise ve team_lead attribute'u yoksa, ekle
        if isinstance(obj, ProjectFile) and not hasattr(obj, 'team_lead'):
            obj.team_lead = obj.project.team_lead
        super().check_object_permissions(request, obj)

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db.models import Q
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer
from .permissions import IsTeamLeadOrAdmin  # permissions.py içindeki izinleriniz


# --- Task Oluşturma ---
# POST /task-add/
# Yalnızca admin veya team_lead görevi oluşturabilir.
class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        project = serializer.validated_data['project']
        user = self.request.user

        # Sadece admin veya project.team_lead görev oluşturabilir
        if not (user.is_superuser or project.team_lead == user):
            raise PermissionDenied("Ekleme yetkiniz yok.")

        serializer.save(assigned_by=user)

# --- Task Listeleme ---
# GET /tasks/
# Projede erişimi olan kullanıcılar (team_lead, team_members veya assigned_to) görevleri görebilir.
class TaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(
            Q(assigned_to=user) |
            Q(assigned_by=user) |
            Q(project__team_lead=user) |
            Q(project__team_members=user, assigned_to=user)
        ).distinct()



# --- Task Detay ---
# GET /tasks/<int:pk>/
class TaskDetailView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        user = self.request.user

        # Admin her şeyi görebilir
        if user.is_superuser:
            return obj

        # Proje üyeleri ve assigned_to kullanıcıları görevleri görebilir
        if obj.project.team_lead == user or user in obj.project.team_members.all() or obj.assigned_to == user:
            return obj

        # Yetkisiz erişim
        raise PermissionDenied("Bu görevi görüntüleme yetkiniz yok.")
# --- Task Güncelleme ---
# PUT/PATCH /tasks/<int:pk>/update/
# Admin ve team_lead tüm alanları güncelleyebilir;
# Görev atanan (assigned_to) kullanıcı sadece status alanını güncelleyebilir.
class TaskUpdateView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data.copy()
        user = request.user

        # Proje güncellenemez
        if 'project' in data and str(data['project']) != str(instance.project.id):
            return Response({"error": "Proje bilgisi güncellenemez."}, status=status.HTTP_400_BAD_REQUEST)

        is_team_lead = instance.project.team_lead == user
        is_assigned_by = instance.assigned_by == user
        is_assigned_to = instance.assigned_to == user

        # Sadece status güncelleyebilecekse kontrol et
        if is_assigned_to and not (user.is_superuser or is_team_lead or is_assigned_by):
            allowed_fields = {'status'}
            if not set(data.keys()).issubset(allowed_fields):
                return Response({"error": "Sadece görev durumu güncellenebilir."}, status=status.HTTP_403_FORBIDDEN)
            return super().update(request, *args, **kwargs)

        # Admin, team_lead veya assigned_by tüm alanları güncelleyebilir
        if user.is_superuser or is_team_lead or is_assigned_by:
            return super().update(request, *args, **kwargs)

        return Response({"error": "Güncelleme yetkiniz yok."}, status=status.HTTP_403_FORBIDDEN)

# --- Task Silme ---
# DELETE /tasks/<int:pk>/delete/
# Yalnızca admin (superuser) görev silebilir.
class TaskDeleteView(generics.DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAdminUser]