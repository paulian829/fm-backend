from django.contrib import admin
from .models import User
from . import models
# Register your models here.
admin.site.register(User)
admin.site.register(models.Images)
admin.site.register(models.Camera)
admin.site.register(models.Reports)



