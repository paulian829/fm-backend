from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=30)
    bio = models.CharField(max_length=30)
    
    def __str__(self):
        return self.fname
    def __str__(self):
        return self.lname

class Task(models.Model):
    title = models.CharField(max_length=200,null=False)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


    
   