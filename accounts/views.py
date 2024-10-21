from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

from .forms import CustomUserCreationForm
from .models import CustomUser, AcademicSession
from .decorators import authenticate_check


@authenticate_check
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        academic_session = request.POST['academic_session']

        user: CustomUser = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_student:
                user_role = 'student'
            elif user.is_teacher:
                user_role = 'teacher'
            elif user.is_principal:
                user_role = 'principal'
            else:
                user_role = None

            if user_role:
                user_session = getattr(user, user_role).academic_session.year

                if academic_session == user_session:
                    login(request, user)
                    return redirect(f'{user_role}_dashboard')
                else:
                    messages.error(request, "Your login credentials are not for this year.")
            else:
                messages.error(request, "Invalid login credentials.")
        else:
            messages.error(request, "Invalid username or password.")

    academic_sessions = AcademicSession.objects.all()

    return render(request, 'registration/login.html', context={'academic_sessions': academic_sessions})


# def logout(request):


def student_signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            current_session = AcademicSession.objects.get(current=True)

            obj: CustomUser = form.save(commit=False)
            obj.is_student = True
            obj.academic_session = current_session
            obj.save()
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/student_create.html', context={'form': form})


def teacher_signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            current_session = AcademicSession.objects.get(current=True)

            obj: CustomUser = form.save(commit=False)
            obj.is_teacher = True
            obj.academic_session = current_session
            obj.save()
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/teacher_create.html', context={'form': form})
