from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Project
from .serializers import ProjectSerializer
from rest_framework.permissions import IsAdminUser
from .permissions import IsTeamLeadOrAdmin, CanListProjects
from django.db.models import Q  # Q nesnesini doğrudan import edelim


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
    permission_classes = [IsAuthenticated]

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
