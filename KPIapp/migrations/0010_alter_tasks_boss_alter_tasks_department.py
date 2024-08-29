# Generated by Django 4.2.15 on 2024-08-25 11:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('KPIapp', '0009_alter_tasks_mark'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='boss',
            field=models.ForeignKey(default='Appointed', on_delete=django.db.models.deletion.CASCADE, related_name='boss', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='department',
            field=models.ForeignKey(default='Departments', on_delete=django.db.models.deletion.CASCADE, related_name='department', to='KPIapp.departments'),
        ),
    ]
