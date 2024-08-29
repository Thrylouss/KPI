# Generated by Django 4.2.15 on 2024-08-23 12:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('KPIapp', '0005_alter_user_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='departments',
            name='responsible',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.AUTH_USER_MODEL),
        ),
    ]
