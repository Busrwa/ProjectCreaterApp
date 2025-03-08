# Generated by Django 4.2.19 on 2025-03-05 19:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("projectCreater", "0002_rename_proje_projectcreater"),
    ]

    operations = [
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "internal_external",
                    models.CharField(
                        choices=[("Internal", "Internal"), ("External", "External")],
                        default="External",
                        max_length=10,
                    ),
                ),
                ("kurum", models.CharField(max_length=255)),
                ("telefon", models.CharField(max_length=15)),
                ("son_teslim_tarihi", models.DateField()),
                (
                    "sorumlu_ekip",
                    models.ManyToManyField(
                        related_name="projeler", to=settings.AUTH_USER_MODEL
                    ),
                ),
                (
                    "sorumlu_ekip_uyesi",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="projectCreater",
        ),
        migrations.DeleteModel(
            name="SorumluEkip",
        ),
    ]
