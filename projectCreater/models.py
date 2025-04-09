from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from accounts.models import CrudUser


class Project(models.Model):
    INTERNAL_EXTERNAL_CHOICES = [
        ('internal', 'Internal'),
        ('external', 'External')
    ]

    internal_external = models.CharField(max_length=10, choices=INTERNAL_EXTERNAL_CHOICES)
    organisation = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    team_lead = models.ForeignKey(User, on_delete=models.CASCADE)
    team_members = models.ManyToManyField(User, related_name="team_members")
    last_delivery_date = models.DateField()

    # Yeni Alanlar
    description = models.TextField(blank=True, null=True)  # Açıklama
    description_added_date = models.DateTimeField(auto_now_add=True)  # Açıklamanın eklenme tarihi

    def __str__(self):
        return self.organisation

#dosya yüklemeyi ayrı yapıyoruz
class ProjectFile(models.Model):
    project = models.ForeignKey(Project, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='project_files/')  # Dosyalar 'project_files/' klasörüne yüklenecek
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File {self.file.name} for {self.project.organisation}"

    def clean(self):
        if self.project.team_lead != self.uploaded_by and self.uploaded_by not in self.project.team_members.all() and not self.uploaded_by.is_superuser:
            raise ValidationError("Only team lead, team members, or admin can upload files.")


class Task(models.Model):
    title = models.CharField(max_length=255)
    assigned_by = models.ForeignKey(User, related_name='tasks_assigned', on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, related_name='tasks_received', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    message = models.TextField()

    STATUS_CHOICES = [
        ('todo', 'Tamamlanması Gerekiyor'),
        ('completed', 'Tamamlandı'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    project = models.ForeignKey('Project', related_name='tasks',
                                on_delete=models.CASCADE)  # Project modeline ForeignKey

    def __str__(self):
        return self.title