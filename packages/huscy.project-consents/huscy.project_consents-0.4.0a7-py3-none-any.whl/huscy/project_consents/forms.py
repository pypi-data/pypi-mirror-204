from django import forms
from django.core.exceptions import ValidationError

from huscy.projects.models import Project
from huscy.subjects.models import Subject


class ProjectChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, project):
        return project.title


class TokenForm(forms.Form):
    project = ProjectChoiceField(queryset=Project.objects.all())
    subject = forms.UUIDField()

    def clean_subject(self):
        subject_id = self.cleaned_data['subject']
        try:
            subject = Subject.objects.get(pk=subject_id)
        except Subject.DoesNotExist:
            raise ValidationError('subject does not exist')
        return subject
