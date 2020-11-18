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


class DownloadDocumentForm(forms.Form):
    format_choices = (
        ("pdf", "PDF Format"),
        ("png", "PNG Format"),
        ("jpg", "JPG Format"),
    )
    document_id = forms.CharField(label='document_id', max_length=100)
    format = forms.ChoiceField(label='format', choices=format_choices)