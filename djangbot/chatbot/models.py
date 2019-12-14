from django.db import models

# Create your models here.

class Files(models.Model):
    id = models.IntegerField(primary_key=True)
    url = models.TextField()

    def __str__(self):
        return self.url