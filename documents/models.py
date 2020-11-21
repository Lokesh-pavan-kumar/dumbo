from django.db import models
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager
from django.db.models.signals import pre_delete
from google.cloud import storage
import os
from dumbo.settings import BASE_DIR
from datetime import date
from django.core.signals import request_finished

User = get_user_model()


def update_filename(instance, filename):
    # instance : A model instance type: documents.models.Document
    # filename : The original name of the file(in user's local machine) type: str
    extension = filename.split('.')[-1]  # Get the file extension from the original filename
    new_filename = '_'.join(instance.name.split())  # name assigned to the document by the user
    updated_filename = f'documents/{new_filename}.{extension}'  # Complete storage path of the document
    print(f'Saving File to : {updated_filename}')
    return updated_filename


class Document(models.Model):
    name = models.CharField(max_length=255, verbose_name='Name of the document')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    path = models.FileField(upload_to=update_filename)  # URL := gs://{bucket-name}/{file-path}
    date_added = models.DateField(auto_now_add=True)
    last_updated = models.DateField(auto_now=True)
    expiry_date = models.DateField(null=True, blank=True)
    # tags = models.TextField(null=True, blank=True)
    tags = TaggableManager()
    is_public = models.BooleanField()
    is_important = models.BooleanField()
    in_trash = models.BooleanField(default=False)
    view_count = models.IntegerField(default=0)

    def __str__(self):
        owner_name = self.owner.username
        return f"{owner_name}'s {self.name}"


class thumbs(models.Model):
    id = models.OneToOneField(Document, on_delete=models.CASCADE, primary_key=True)
    image = models.ImageField(
        default='https://storage.googleapis.com/dumbo-document-storage/thumbnails/documents/default.jpg',
        upload_to='thumbnails/')


def delete_blob(sender, instance, **kwargs):
    print('Entered PreDelete')
    if os.environ.get('GOOGLE_APPLICATION_CREDENTIALS') is None:
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(BASE_DIR, 'credential.json')
    storage_client = storage.Client()
    bucket = storage_client.bucket('dumbo-document-storage')
    blob_name = instance.path.name
    blob = bucket.blob(blob_name)
    if blob.exists():
        blob.delete()


pre_delete.connect(delete_blob, sender=Document)


def after_request(sender, **kwargs):
    documents = Document.objects.all()
    for doc in documents:
        if not doc.in_trash and doc.expiry_date is not None:
            doc.in_trash = date.today() > doc.expiry_date
            doc.save()


request_finished.connect(after_request)
