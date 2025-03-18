from django.db import models
from django.contrib.auth.models import User

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
