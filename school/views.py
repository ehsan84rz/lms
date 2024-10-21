from datetime import datetime, timedelta, date

from jalali_date import date2jalali

from django.http import HttpResponse, JsonResponse
from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.views import login_required
from django.db.models import Sum
from django.db.models.functions import ExtractIsoWeekDay, ExtractWeekDay

from accounts.models import AcademicSession
from .models import Class, Student, Exam, Score, RollCall, RollCallRecord, Teacher, AssignedTeachers, Task, StudyTime, \
    Lesson, Assignment, AssignmentRecord
from .forms import SearchForUser, ScoreFormSet, RollCallRecordForm, ClassCreateForm, TaskCreateForm, \
    AssignmentCreateForm, AssignmentRecordForm


@login_required()
def student_dashboard(request):
    return render(request, 'student/dashboard.html')


@login_required()
def teacher_dashboard(request):
    return render(request, 'teacher/dashboard.html')


def class_list_view(request):
    queryset = Class.objects.all()

    if request.method == 'POST':
        form = ClassCreateForm(request.POST)
        if form.is_valid():
            current_session = AcademicSession.objects.get(current=True)
            obj: Class = form.save(commit=False)
            obj.academic_session = current_session
            obj.save()
            redirect('class_list')

    form = ClassCreateForm()
    return render(request, 'class/list.html', context={'classes': queryset, 'form': form})


def class_detail(request, pk):
    current_class = get_object_or_404(Class, pk=pk)
    students_in_class = Student.objects.filter(current_class=current_class).select_related('user')
    assigned_teachers_in_class = AssignedTeachers.objects.filter(current_class=current_class)

    form = SearchForUser()

    context = {
        'class_instance': current_class,
        'students_in_class': students_in_class,
        'assigned_teachers_in_class': assigned_teachers_in_class,
        'form': form,
    }

    return render(request, 'class/detail.html', context)


def class_add_students(request, pk):
    current_class = get_object_or_404(Class, pk=pk)

    if request.method == 'POST':
        form = SearchForUser(request.POST)
        if form.is_valid():
            student = form.cleaned_data['username']
            query = Student.objects.filter(user__username=student)
            if query.exists():
                query.update(current_class=current_class)
                return redirect('class_detail', current_class.pk)
            else:
                messages.error(request, 'This Student does not exist/This user is not a Student')
                return redirect('class_detail', current_class.pk)
        else:
            messages.error(request, 'The provided Nat_ID is not valid')
            return redirect('class_detail', current_class.pk)
    else:
        return HttpResponse(status=405)


def class_add_teachers(request, pk):
    current_class = get_object_or_404(Class, pk=pk)

    if request.method == 'POST':
        form = SearchForUser(request.POST)
        if form.is_valid():
            teacher_username = form.cleaned_data['username']
            try:
                teacher = Teacher.objects.get(user__username=teacher_username)
            except Teacher.DoesNotExist:
                messages.error(request, 'This Teacher does not exist/This user is not a Teacher')
                return redirect('class_detail', current_class.pk)

            if AssignedTeachers.objects.filter(teacher=teacher, current_class=current_class).exists():
                messages.error(request, 'This teacher was assigned to the class')
            else:
                AssignedTeachers.objects.create(teacher=teacher, current_class=current_class)
                return redirect('class_detail', current_class.pk)
        else:
            messages.error(request, 'The provided Nat_ID is not valid')
    else:
        return HttpResponse(status=405)

    return redirect('class_detail', current_class.pk)


def exam_list_view(request):
    queryset = Exam.objects.all()
    return render(request, 'exam/list.html', context={'exams': queryset})


def exam_detail(request, pk):
    exam = Exam.objects.get(pk=pk)
    students = Student.objects.filter(current_class=exam.exam_class).select_related('user')
    scores = Score.objects.filter(exam=exam).select_related('student')

    if request.method == 'POST':
        formset = ScoreFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                print(form.cleaned_data)
                student_id = form.cleaned_data.get('student_id')
                # student_name = form.cleaned_data.get('student_name')
                obtained_score = form.cleaned_data.get('obtained_score')

                # Find the corresponding student based on the name
                student = Student.objects.get(pk=student_id)

                # Get or create the Score object
                score, created = Score.objects.get_or_create(exam=exam, student=student,
                                                             defaults={'obtained_score': obtained_score})

                # Update the obtained score
                score.obtained_score = obtained_score
                score.save()
            return redirect('exam_detail', exam.id)
        else:
            messages.error(request, 'Something is wrong with provided information')

    else:
        initial_data = []
        scores_dict = {score.student.id: score.obtained_score for score in scores}
        for student in students:
            initial_data.append(
                {'student_id': student.id, 'student_name': student, 'obtained_score': scores_dict.get(student.id, 0)})
        # print(initial_data)
        formset = ScoreFormSet(initial=initial_data)

    return render(request, 'exam/detail_and_Score.html', {'exam': exam, 'formset': formset})


def roll_call_list(request):
    # queryset = RollCall.objects.filter(current_class=request) TODO: define current_class in sessions and check it here
    roll_calls = RollCall.objects.all()
    return render(request, 'rollcall/list.html', context={'roll_calls': roll_calls})


def roll_call_detail(request, pk):
    roll_call = RollCall.objects.get(pk=pk)
    students = Student.objects.filter(current_class=roll_call.current_class).select_related('user')
    roll_call_records = RollCallRecord.objects.filter(roll_call=roll_call)

    RollCallRecordFormSet = forms.formset_factory(RollCallRecordForm, extra=0, can_delete=False)

    if request.method == 'POST':
        formset = RollCallRecordFormSet(request.POST)
        if formset.is_valid():  # TODO: and formset.has_changed()
            for form in formset:
                student_id = form.cleaned_data['student_id']
                status = form.cleaned_data['status']

                student = Student.objects.get(pk=student_id)

                record, created = RollCallRecord.objects.get_or_create(roll_call=roll_call, student=student,
                                                                       defaults={'status': status})

                record.status = status
                record.save()

            return redirect('rollcall_detail', roll_call.id)

        else:
            messages.error(request, 'Something is wrong with provided information')

    initial_data = []
    roll_call_records_dict = {roll_cal_record.id: roll_cal_record.status for roll_cal_record in roll_call_records}
    for student in students:
        student_id = student.id
        initial_status = roll_call_records_dict.get(student_id, 'present')
        initial_data.append(
            {'student_id': student_id, 'student_name': student.user.get_full_name(), 'status': initial_status}
        )

    formset = RollCallRecordFormSet(initial=initial_data)

    context = {
        'roll_call': roll_call,
        'records': roll_call_records,
        'formset': formset
    }

    return render(request, 'rollcall/detail_and_Record.html', context=context)


def task_list_view(request, class_num):
    current_class = get_object_or_404(Class, name=class_num)
    tasks = Task.objects.filter(current_class=current_class).all()

    persian_weekday_names = {
        'Saturday': 'شنبه',
        'Sunday': 'یک‌شنبه',
        'Monday': 'دوشنبه',
        'Tuesday': 'سه‌شنبه',
        'Wednesday': 'چهارشنبه',
        'Thursday': 'پنج‌شنبه',
        'Friday': 'جمعه',
    }

    # Group tasks by weekday
    tasks_by_weekday = {}
    for task in tasks:
        day_name = persian_weekday_names.get(
            date2jalali(task.task_date).strftime('%A'))  # Get the full name of the weekday
        print(date2jalali(task.task_date))
        tasks_by_weekday.setdefault(day_name, []).append(task)
    print(tasks_by_weekday)

    # Sort tasks within each weekday by task_date
    for tasks_list in tasks_by_weekday.values():
        tasks_list.sort(key=lambda x: x.task_date)

    if request.method == 'POST':
        form = TaskCreateForm(request.POST)
        if form.is_valid():
            obj: Task = form.save(commit=False)
            obj.current_class = current_class
            obj.save()
            messages.success(request, 'The task has successfully added')
            return redirect('task_list', class_num)

    form = TaskCreateForm()
    return render(request, 'task/list.html',
                  context={'form': form, 'class': current_class, 'tasks_by_weekday': tasks_by_weekday, 'tasks': tasks})


def get_week_date_range(date):
    # Find the day of the week (0 = Monday, 6 = Sunday)
    day_of_week = date.weekday()

    # Calculate the difference between the current day and the next Saturday (5)
    days_until_saturday = 7 - (5 - day_of_week) % 7

    # Calculate the starting date of the week (Saturday)
    start_date = date - timedelta(days=days_until_saturday)

    # Calculate the ending date of the week (Friday)
    end_date = start_date + timedelta(days=6)

    return start_date, end_date


def study_time_view(request):
    current_date = datetime.now().date()
    start_date, end_date = get_week_date_range(current_date)
    user = Student.objects.get(user__username=request.user.username)
    current_class = get_object_or_404(Class, pk=user.current_class_id)
    teachers_in_class = current_class.teachers.all()
    lessons = Lesson.objects.filter(teachers__in=teachers_in_class)
    print(lessons)
    study_times = StudyTime.objects.filter(student=user, date__range=(start_date, end_date)).select_related('lesson')
    # # Organize study times by lesson and day of the week
    # lesson_data = {}
    # for study_time in study_times:
    #     lesson_id = study_time.lesson.id
    #     day_of_week = 7 - (6 - study_time.date.isoweekday()) % 7  # 0 for Saturday, 1 for Sunday, etc.
    #
    #     if lesson_id not in lesson_data:
    #         lesson_data[lesson_id] = {
    #             'lesson': study_time.lesson,
    #             'study_times': [0] * 7,  # Initialize list for each day of the week
    #             'total_time': 0,
    #         }
    #
    #     lesson_data[lesson_id]['study_times'][day_of_week] += study_time.amount
    #     lesson_data[lesson_id]['total_time'] += study_time.amount

    # Initialize lesson_data with all lessons
    lesson_data = {lesson.id: {'lesson': lesson, 'study_times': [0] * 7, 'total_time': 0} for lesson in lessons}
    print(lesson_data)

    for study_time in study_times:
        lesson_id = study_time.lesson.id
        day_of_week = 7 - (6 - study_time.date.isoweekday()) % 7  # 0 for Saturday, 1 for Sunday, etc.

        lesson_data[lesson_id]['study_times'][day_of_week] += study_time.amount
        lesson_data[lesson_id]['total_time'] += study_time.amount
    # Prepare context for the template
    context = {
        'lesson_data': lesson_data,
        'days_of_week': ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
    }
    return render(request, 'study_time/list.html', context=context)


def test(request):
    if request.method == 'GET':
        data = {'hello': 'hi'}
        modal_title = f"Modal Title: {data['folk']}"
        response = JsonResponse(data, safe=False)
        response['HX-Swap-After'] = f"#modal-title:{modal_title}"

        return response


def assignment_list(request):
    teacher = Teacher.objects.get(user=request.user)
    assignments = Assignment.objects.filter(teacher=teacher)

    if request.method == 'POST':
        form = AssignmentCreateForm(request.POST)
        if form.is_valid():
            obj: Assignment = form.save(commit=False)
            obj.teacher = teacher
            obj.save()

    form = AssignmentCreateForm()
    form.fields['lesson'].queryset = Lesson.objects.filter(teachers=teacher)
    form.fields['assigned_class'].queryset = Class.objects.filter(teachers=teacher)

    context = {
        'teacher': teacher,
        'assignments': assignments,
        'form': form
    }
    return render(request, 'assignment/list.html', context=context)


def assignment_detail(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    assignments = AssignmentRecord.objects.filter(assignment=assignment)
    students = Student.objects.filter(current_class_id=assignment.assigned_class.id)

    AssignmentRecordFormSet = forms.formset_factory(AssignmentRecordForm, extra=0)

    if request.method == 'POST':
        formset = AssignmentRecordFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                student_id = form.cleaned_data['student_id']
                reason = form.cleaned_data['reason']
                status = form.cleaned_data['status']

                form_student = Student.objects.get(pk=student_id)

                assignment_record = assignments.get(student=form_student)  # TODO: Meta: unique_together

                assignment_record.reason = reason
                assignment_record.status = status

                assignment_record.save()
                return redirect('assignment_detail', pk)

    initial_data = []
    assignment_records_dict = {
        assignment_record.student_id: (assignment_record.status, assignment_record.file.url, assignment_record.notes, assignment_record.reason)
        for assignment_record in assignments}
    for student in students:
        student_id = student.id
        initial_set = assignment_records_dict.get(student_id, ('I', '', '', ''))
        initial_status = initial_set[0]
        initial_file_url = initial_set[1]
        initial_note = initial_set[2]
        initial_reason = initial_set[3]
        initial_data.append(
            {
                'student_id': student_id,
                'student_name': student.user.get_full_name(),
                'status': initial_status,
                'file': initial_file_url,
                'note': initial_note,
                'reason': initial_reason,
            }
        )

    formset = AssignmentRecordFormSet(initial=initial_data)

    context = {
        'assignment': assignment,
        'students': students,
        'formset': formset,
    }

    return render(request, 'assignment/detail.html', context=context)
