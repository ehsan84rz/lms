from jdatetime.jalali import GregorianToJalali

from django.db import models

from accounts.models import CustomUser, AcademicSession


class Lesson(models.Model):
    name = models.CharField(max_length=20)

    teachers = models.ManyToManyField('Teacher', through='LessonedTeachers', blank=True, related_name='lessons')

    academic_session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Class(models.Model):
    name = models.CharField(max_length=50, unique=True)

    teachers = models.ManyToManyField('Teacher', through='AssignedTeachers', blank=True, related_name='classes')

    academic_session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)  # user.student
    current_class = models.ForeignKey(Class, on_delete=models.CASCADE, null=True, blank=True, related_name='students')

    academic_session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name()


class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)  # user.teacher

    academic_session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name()


#  TODO: dobare raftam tooe matrix ManyToManyField ha. har Teacher <-> Class, Teacher <-> Lesson
#   Update: Fekr konam dar oomadam az Matrix


class AssignedTeachers(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    current_class = models.ForeignKey(Class, on_delete=models.CASCADE)


class LessonedTeachers(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.teacher} | {self.lesson}'


class Principal(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)  # user.principle

    academic_session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name()


class Exam(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='exams')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='exams')

    name = models.CharField(max_length=255)
    date = models.DateField()
    exam_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    max_score = models.IntegerField()

    academic_session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} on {self.date.month}-{self.date.day}'


class Score(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='scores')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    obtained_score = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.student} | {self.obtained_score} | {self.exam}'


class RollCall(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    name = models.CharField(max_length=255, blank=True)
    current_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    class_date = models.DateField()

    academic_session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)

    def __str__(self):
        if self.name != '':
            return self.name

        return str(self.class_date)

    def save(self, *args, **kwargs):
        if self.name == '':
            self.name = str(self.class_date)  #  TODO: Add lesson

        return super().save(*args, **kwargs)


class RollCallRecord(models.Model):
    STATUS_CHOICES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
    )

    roll_call = models.ForeignKey(RollCall, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f'{self.student} | {self.status} | {self.roll_call}'


class StudyTime(models.Model):
    STUDY_TYPE_CHOICES = (
        ('PS', 'Pre-Study'),
        ('ST', 'Study'),
        ('EX', 'Exercise Solving'),
        ('RV', 'Review'),
        ('AS', 'Assignment'),
        ('EV', 'Educational Video'),
        ('TS', 'Test'),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    study_type = models.CharField(max_length=2, choices=STUDY_TYPE_CHOICES)
    amount = models.PositiveSmallIntegerField()
    date = models.DateField()
    #  TODO: Define StudyTime views and urls

    def __str__(self):
        return f'{self.student.user.get_full_name()} | {self.amount} | {self.lesson.name}'


class Task(models.Model):
    title = models.CharField(max_length=50)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    current_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    task_date = models.DateField()

    def jalali_task_date(self):
        jalali_date = GregorianToJalali(self.task_date)
        day_name = jalali_date.strftime('%A')
        month_name = jalali_date.strftime('%B')

        # Mapping Persian month names
        persian_month_names = {
            'Farvardin': 'فروردین',
            'Ordibehesht': 'اردیبهشت',
            'Khordad': 'خرداد',
            'Tir': 'تیر',
            'Mordad': 'مرداد',
            'Shahrivar': 'شهریور',
            'Mehr': 'مهر',
            'Aban': 'آبان',
            'Azar': 'آذر',
            'Dey': 'دی',
            'Bahman': 'بهمن',
            'Esfand': 'اسفند',
        }

        # Mapping Persian weekday names
        persian_weekday_names = {
            'Saturday': 'شنبه',
            'Sunday': 'یک‌شنبه',
            'Monday': 'دوشنبه',
            'Tuesday': 'سه‌شنبه',
            'Wednesday': 'چهارشنبه',
            'Thursday': 'پنج‌شنبه',
            'Friday': 'جمعه',
        }

        jalali_month_name = persian_month_names.get(month_name, month_name)
        jalali_weekday_name = persian_weekday_names.get(day_name, day_name)

        return f'{jalali_weekday_name} {jalali_date.day} {jalali_month_name} {jalali_date.year}'


class Assignment(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    assigned_class = models.ForeignKey(Class, on_delete=models.CASCADE)

    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    assignment_datetime = models.DateTimeField()


class AssignmentRecord(models.Model):
    ASSIGNMENT_STATUS = (
        ('D', 'Done'),
        ('F', 'Failure'),
        ('I', 'Incomplete'),
    )

    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    file = models.FileField(upload_to='assignments/', blank=True, null=True)
    notes = models.CharField(max_length=750, blank=True)
    reason = models.CharField(max_length=750, blank=True)
    status = models.CharField(max_length=1, choices=ASSIGNMENT_STATUS, default='I')
