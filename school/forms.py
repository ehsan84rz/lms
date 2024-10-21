from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime

from django import forms
from django.forms import BaseFormSet

from .models import Score, RollCallRecord, Class, Task, Assignment, AssignmentRecord


class SearchForUser(forms.Form):
    username = forms.CharField(max_length=10)


class ScoreForm(forms.Form):
    student_id = forms.IntegerField(widget=forms.HiddenInput)
    student_name = forms.CharField(max_length=255, required=False, disabled=True)
    obtained_score = forms.IntegerField(required=False)

    # def __init__(self, *args, **kwargs):
    #     instance = kwargs.pop('instance', None)
    #     super().__init__(*args, **kwargs)
    #     if instance and instance.student:
    #         # self.fields['student_name'].initial = instance.student.name
    #         # self.fields['student_name'].widget.attrs['readonly'] = True
    #
    #         self.fields['student_id'].initial = instance.student.id
    #         self.fields['student_id'].widget.attrs['hidden'] = True


# class BaseScoreFormSet(BaseFormSet):
#     def __init__(self, *args, **kwargs):
#         self.queryset = kwargs.pop('queryset', None)
#         super().__init__(*args, **kwargs)


ScoreFormSet = forms.formset_factory(ScoreForm, extra=0)


# TODO: Define BaseScoreFormSet for custom validation https://www.youtube.com/watch?v=i6VbAob9GgQ


class RollCallRecordForm(forms.Form):
    student_id = forms.IntegerField(widget=forms.HiddenInput)
    student_name = forms.CharField(max_length=255, required=False, disabled=True)
    status = forms.ChoiceField(choices=RollCallRecord.STATUS_CHOICES)


class ClassCreateForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ('name', 'teachers')


class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'lesson', 'description', 'task_date')
        # widgets = {
        #     'task_date': forms.DateInput(attrs={'type': 'date', 'placeholder': 'yyyy-mm-dd'})
        # }

    def __init__(self, *args, **kwargs):
        super(TaskCreateForm, self).__init__(*args, **kwargs)
        self.fields['task_date'] = JalaliDateField(label='date',  # date format is  "yyyy-mm-dd"
                                                   widget=AdminJalaliDateWidget  # optional, to use default datepicker
                                                   )


class AssignmentCreateForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ('title', 'lesson', 'description', 'assignment_datetime', 'assigned_class')

    def __init__(self, *args, **kwargs):
        super(AssignmentCreateForm, self).__init__(*args, **kwargs)
        self.fields['assignment_datetime'] = SplitJalaliDateTimeField(label='Assignment Date and Time',
                                                                      widget=AdminSplitJalaliDateTime
                                                                      )


class AssignmentRecordForm(forms.Form):
    student_id = forms.IntegerField(widget=forms.HiddenInput)
    student_name = forms.CharField(max_length=255, required=False, disabled=True)
    file = forms.CharField(disabled=True, required=False)
    note = forms.CharField(max_length=750, disabled=True, required=False)
    reason = forms.CharField(max_length=750, required=False)
    status = forms.ChoiceField(choices=AssignmentRecord.ASSIGNMENT_STATUS)

