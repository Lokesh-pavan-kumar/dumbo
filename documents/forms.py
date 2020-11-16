from django import forms
from .models import Document


class UploadDocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['name', 'is_important', 'is_public', 'path']


class DocumentUpdateForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['is_public', 'is_important', 'expiry_date', 'tags']