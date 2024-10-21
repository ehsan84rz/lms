from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from school.models import Student, Teacher, Principal

from .models import AcademicSession, CustomUser


@receiver(post_save, sender=AcademicSession)
def after_saving_session(sender, created, instance: AcademicSession, *args, **kwargs):
    """Change all academic sessions to false if this is true"""
    if instance.current is True:
        AcademicSession.objects.exclude(pk=instance.id).update(current=False)


@receiver(post_save, sender=CustomUser)
def active_user_profile(sender, created, instance: CustomUser, *args, **kwargs):
    """Active user's profile"""
    if instance.is_student is True and Student.objects.filter(user_id=instance.id).exists() is not True:
        Student.objects.create(
            user=instance, academic_session=instance.academic_session
        )
    if instance.is_teacher is True and Teacher.objects.filter(user_id=instance.id).exists() is not True:
        Teacher.objects.create(
            user=instance, academic_session=instance.academic_session
        )
    if instance.is_principal is True and Principal.objects.filter(user_id=instance.id).exists() is not True:
        Principal.objects.create(
            user=instance, academic_session=instance.academic_session
        )
