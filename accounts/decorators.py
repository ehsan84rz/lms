from django.shortcuts import redirect


def check_role(request):
    if request.user.is_student is not True:
        if request.user.is_teacher is not True:
            return 'principal'
        return 'teacher'
    return 'student'


def redirect_dashboard(request):
    return redirect(f'{check_role(request)}_dashboard')


def authenticate_check(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect_dashboard(request)
        else:
            # If not authenticated, you can add additional logic here if needed
            pass

        return view_func(request, *args, **kwargs)

    return wrapper
