# Generated by Django 4.2.7 on 2023-12-16 16:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0003_rename_task_datetime_assignment_assignment_datetime'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assignment',
            old_name='current_class',
            new_name='assigned_class',
        ),
    ]