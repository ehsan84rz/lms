from django.contrib import admin

from .models import Class, Exam, Score, RollCall, RollCallRecord, Student, Lesson, Teacher, Principal, AssignedTeachers, \
    LessonedTeachers, Task, StudyTime, Assignment, AssignmentRecord


class ClassStudentsInline(admin.TabularInline):
    model = Student


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    fields = ('name', 'academic_session')
    inlines = [ClassStudentsInline]


class LessonedTeachersInline(admin.TabularInline):
    model = LessonedTeachers


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    inlines = [LessonedTeachersInline]


# admin.site.register(Lesson)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(AssignedTeachers)
admin.site.register(LessonedTeachers)
admin.site.register(Principal)
admin.site.register(Exam)
admin.site.register(Score)
admin.site.register(RollCall)
admin.site.register(RollCallRecord)
admin.site.register(Task)
admin.site.register(Assignment)
admin.site.register(AssignmentRecord)
admin.site.register(StudyTime)
