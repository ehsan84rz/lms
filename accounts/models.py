import os.path

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from config import settings
from .validators import is_valid_national_code


class CustomUser(AbstractUser):
    academic_session = models.ForeignKey('AcademicSession', on_delete=models.CASCADE, null=True, blank=True)

    username = models.CharField(verbose_name='کد ملی', max_length=10, unique=True, validators=[is_valid_national_code])
    first_name = models.CharField(verbose_name='نام',  max_length=150, blank=True)
    last_name = models.CharField(verbose_name='نام خانوادگی', max_length=150, blank=True)
    email = models.EmailField(null=True, blank=True)
    religion = models.CharField(max_length=20, default='اسلام')
    profile_image = models.ImageField(upload_to='accounts/profile_image/', blank=True)

    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_principal = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_role(self):
        if self.is_student:
            return 'student'
        elif self.is_teacher:
            return 'teacher'
        else:
            return 'principal'

    def get_profile_image(self):
        if not self.profile_image:
            return os.path.join(settings.STATIC_URL, f'img/figure/{self.get_role()}.png/')
        return self.profile_image.url


class AcademicSession(models.Model):
    year = models.CharField(max_length=9, unique=True)
    current = models.BooleanField(default=True)

    def __str__(self):
        return self.year

# class UserProfile(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile', primary_key=True)
#     bio = models.CharField(max_length=350)
#
#     def __str__(self):
#         return self.user.username
