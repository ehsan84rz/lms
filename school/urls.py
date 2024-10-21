from django.urls import path

from . import views


urlpatterns = [
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),

    path('classes/', views.class_list_view, name='class_list'),
    path('class/<int:pk>/', views.class_detail, name='class_detail'),
    path('class/<int:pk>/add-student', views.class_add_students, name='class_add_student'),
    path('class/<int:pk>/add-teacher', views.class_add_teachers, name='class_add_teacher'),

    path('exams/', views.exam_list_view, name='exam_list'),
    path('exam/<int:pk>/', views.exam_detail, name='exam_detail'),

    path('rollcalls/', views.roll_call_list, name='rollcall_list'),
    path('rollcall/<int:pk>/', views.roll_call_detail, name='rollcall_detail'),

    path('tasks/<str:class_num>/', views.task_list_view, name='task_list'),

    path('study_times/', views.study_time_view, name='study_time_list'),
    path('study_times/test/', views.test, name='test'),

    path('assignments/', views.assignment_list, name='assignment_list'),
    path('assignment/<int:pk>/', views.assignment_detail, name='assignment_detail'),

]
