from django.db import models

# Create your models here.

class Tasks(models.Model):
    task = models.CharField(max_length=300)
    done = models.BooleanField(default=False)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.task