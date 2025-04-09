from rest_framework import serializers
from .models import Project, ProjectFile, Task  # Task modelini de dahil ettik
from .permissions import IsTeamLeadOrAdmin

class ProjectFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectFile
        fields = ['id', 'file', 'uploaded_by', 'uploaded_at']
        read_only_fields = ('uploaded_by', 'uploaded_at')


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('assigned_by',)  # Eğer assigned_by otomatik doldurulacaksa


class ProjectSerializer(serializers.ModelSerializer):
    files = ProjectFileSerializer(many=True, read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)  # Task'ları nested olarak ekledik

    class Meta:
        model = Project
        fields = [
            'id',
            'organisation',
            'internal_external',
            'phone',
            'team_lead',
            'team_members',
            'last_delivery_date',
            'description',
            'description_added_date',
            'files',   # Projeye ait dosyalar
            'tasks',   # Projeye ait task'lar (görevler)
        ]