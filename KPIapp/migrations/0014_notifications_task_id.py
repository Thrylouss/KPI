# Generated by Django 4.2.15 on 2024-08-29 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KPIapp', '0013_notifications_url_alter_notifications_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='task_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
