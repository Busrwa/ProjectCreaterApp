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
