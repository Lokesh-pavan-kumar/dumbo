from django.db import models
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager

User = get_user_model()


class Document(models.Model):
    name = models.CharField(max_length=255, verbose_name='Name of the document')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    path = models.FileField(upload_to='documents')  # URL := gs://{bucket-name}/{file-path}
    date_added = models.DateField(auto_now=True)
    last_updated = models.DateField(auto_now_add=True)
    expiry_date = models.DateField(null=True, blank=True)
    # tags = models.TextField(null=True, blank=True)
    tags = TaggableManager()
    is_public = models.BooleanField()
    is_important = models.BooleanField()

    def __str__(self):
        owner_name = self.owner.username
        return f"{owner_name}'s {self.name}"
