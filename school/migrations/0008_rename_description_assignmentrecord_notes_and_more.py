# Generated by Django 4.2.7 on 2023-12-19 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0007_remove_assignmentrecord_is_done_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assignmentrecord',
            old_name='description',
            new_name='notes',
        ),
        migrations.AddField(
            model_name='assignmentrecord',
            name='reason',
            field=models.CharField(blank=True, max_length=750),
        ),
    ]