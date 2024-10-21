# Generated by Django 4.2.7 on 2023-12-11 21:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AssignedTeachers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('academic_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.academicsession')),
            ],
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('max_score', models.IntegerField()),
                ('academic_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.academicsession')),
                ('exam_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.class')),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('academic_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.academicsession')),
            ],
        ),
        migrations.CreateModel(
            name='RollCall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255)),
                ('class_date', models.DateField()),
                ('academic_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.academicsession')),
                ('current_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.class')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.lesson')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('academic_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.academicsession')),
                ('current_class', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='students', to='school.class')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('academic_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.academicsession')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True)),
                ('task_date', models.DateField()),
                ('current_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.class')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.lesson')),
            ],
        ),
        migrations.CreateModel(
            name='StudyTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('study_type', models.CharField(choices=[('PS', 'Pre-Study'), ('ST', 'Study'), ('EX', 'Exercise Solving'), ('RV', 'Review'), ('AS', 'Assignment'), ('EV', 'Educational Video'), ('TS', 'Test')], max_length=2)),
                ('amount', models.PositiveSmallIntegerField()),
                ('date', models.DateField()),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.lesson')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.student')),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('obtained_score', models.IntegerField(blank=True, null=True)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scores', to='school.exam')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.student')),
            ],
        ),
        migrations.CreateModel(
            name='RollCallRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('present', 'Present'), ('absent', 'Absent'), ('late', 'Late')], max_length=10)),
                ('roll_call', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.rollcall')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.student')),
            ],
        ),
        migrations.AddField(
            model_name='rollcall',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.teacher'),
        ),
        migrations.CreateModel(
            name='Principal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('academic_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.academicsession')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LessonedTeachers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.lesson')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.teacher')),
            ],
        ),
        migrations.AddField(
            model_name='lesson',
            name='teachers',
            field=models.ManyToManyField(blank=True, related_name='lessons', through='school.LessonedTeachers', to='school.teacher'),
        ),
        migrations.AddField(
            model_name='exam',
            name='lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exams', to='school.lesson'),
        ),
        migrations.AddField(
            model_name='exam',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exams', to='school.teacher'),
        ),
        migrations.AddField(
            model_name='class',
            name='teachers',
            field=models.ManyToManyField(blank=True, related_name='classes', through='school.AssignedTeachers', to='school.teacher'),
        ),
        migrations.AddField(
            model_name='assignedteachers',
            name='current_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.class'),
        ),
        migrations.AddField(
            model_name='assignedteachers',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.teacher'),
        ),
    ]