from django.db import models
from django.contrib.auth.models import User#, AbstractUser


# def user_directory_path(instance, filename):
#     return 'users/{0}/{1}'.format(instance.username, filename)



# class CustomUser(AbstractUser):
#     image = models.ImageField(upload_to=user_directory_path, blank=True)
    
#     def __str__(self):
#         return str(self.username)


class Tasks(models.Model):
    # task_user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_user = models.CharField(max_length=100)
    task = models.CharField(max_length=300)
    done = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.task