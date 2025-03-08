from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    INTERNAL_EXTERNAL_CHOICES = [
        ('internal', 'Internal'),
        ('external', 'External')
    ]

    internal_external = models.CharField(max_length=10, choices=INTERNAL_EXTERNAL_CHOICES)
    kurum = models.CharField(max_length=255)
    telefon = models.CharField(max_length=20)
    sorumlu_ekip_uyesi = models.ForeignKey(User, on_delete=models.CASCADE)
    sorumlu_ekip = models.ManyToManyField(User, related_name="ekip_uyeleri")
    son_teslim_tarihi = models.DateField()

    def __str__(self):
        return self.kurum
