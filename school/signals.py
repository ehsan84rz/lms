# from django.dispatch import receiver
# from allauth.account.signals import user_signed_up
# from django.contrib.auth.models import Group
#
# from .models import UserProfile
# from jobs.models import Client
#
#
# @receiver(user_signed_up)
# def create_user_profile(request, user, **kwargs):
#     profile = UserProfile(user=user)
#     client_profile = Client(user=user)
#
#     group = Group.objects.get(name='member')
#     user.groups.add(group)
#
#     profile.save()
#     client_profile.save()
