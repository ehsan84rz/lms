from django.contrib import admin

from .models import CustomUser

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, AcademicSession


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_student', 'is_teacher', 'is_principal')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('is_student', 'is_teacher', 'is_principal')}),
    )
    list_display = ['username', 'first_name', 'is_student', 'is_teacher', 'is_principal', 'is_staff']


@admin.register(AcademicSession)
class AcademicSessionAdmin(admin.ModelAdmin):
    ordering = ('-year',)


admin.site.register(CustomUser, CustomUserAdmin)

