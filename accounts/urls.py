from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login_view, name='login-custom'),
    path('students/add/', views.student_signup_view, name='student_create'),
    path('teachers/add/', views.teacher_signup_view, name='teacher_create'),
]
