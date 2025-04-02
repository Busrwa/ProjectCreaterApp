# serializers.py

from rest_framework import serializers
from .models import Project, ProjectFile


class ProjectFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectFile
        fields = ['id', 'file', 'uploaded_by', 'uploaded_at']
        read_only_fields = ('uploaded_by', 'uploaded_at')


class ProjectSerializer(serializers.ModelSerializer):
    # 'related_name' olarak modelde 'files' tanımlandıysa, dosyaları bu alan üzerinden alıyoruz
    files = ProjectFileSerializer(many=True, read_only=True)

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
            'files',  # Projeye ait dosyalar burada listelenecek
        ]
