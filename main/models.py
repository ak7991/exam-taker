from django.db import models

# Create your models here.

class UploadDocument(models.Model):
    title = models.CharField(max_length=100)
    time = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    docfile = models.FileField(upload_to='documents')

    def __str__(self):
        return self.title