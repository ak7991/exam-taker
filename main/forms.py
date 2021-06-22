from django import forms
from django.db.models import fields
from.models import UploadDocument

class DocumentForm(forms.ModelForm):
    class Meta:
        model = UploadDocument
        fields = ('title', 'time', 'description', 'docfile')