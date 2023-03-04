from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class User(models.Model):
    userid = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    department = models.CharField(max_length=30, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=30, null=True)
    postal = models.CharField(max_length=30, null=True)
    country = models.CharField(max_length=30,null=True)
    
    def __str__(self):
        return str(self.userid)
    
class NoFaceMaskImages(models.Model):
    filename = models.CharField(max_length=200, null=True)
    created = models.DateTimeField(auto_now_add=True)


class Images(models.Model):
    filename = models.CharField(max_length=200, null=True)
    path = models.CharField(max_length=200, null=True)
    created = models.DateTimeField(auto_now_add=True)
    source_id = models.ForeignKey('Camera', on_delete=models.SET_NULL, null=True)
    source_ip_address = models.CharField(max_length=200, null=True)
    report_id = models.IntegerField(null=True)
    matched_student_id = models.IntegerField(null=True)
    
    

class Task(models.Model):
    title = models.CharField(max_length=200,null=False)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Camera(models.Model):
    camera_ID = models.AutoField(primary_key=True)
    camera_name = models.CharField(max_length=200, null=True)
    ip_address = models.CharField(max_length=200, null=True)
    camera_details = models.CharField(max_length=200, null=True)
    other_details = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    enabled = models.BooleanField(default=True)
    def __str__(self):
        return self.camera_name
    
   
class Reports(models.Model):
    report_ID = models.AutoField(primary_key=True)
    report_date = models.DateTimeField()
    report_source_images_id = models.CharField(max_length=200, null=True)
    report_source_images_count = models.IntegerField(null=True)
    report_source_images_matched_count = models.IntegerField(null=True)
    unknown_faces_count = models.IntegerField(null=True)
    report_student_id = models.CharField(max_length=200, null=True)
    date_generated = models.DateTimeField(auto_now_add=True)
    output_url = models.CharField(max_length=500, null=True)

class Student(models.Model):
    student_ID = models.AutoField(primary_key=True)
    student_name = models.CharField(max_length=200, null=True)
    student_email = models.CharField(max_length=200, null=True)
    student_contact = models.CharField(max_length=200, null=True)
    student_course = models.CharField(max_length=200, null=True)
    student_section = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    student_image = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.student_name
    
    
class StudentTraniningImage(models.Model):
    student_training_image_ID = models.AutoField(primary_key=True)
    student_ID = models.ForeignKey('Student', on_delete=models.SET_NULL, null=True)
    student_image_filename = models.CharField(max_length=200, null=True)
    student_image_path = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.student_image_filename
    
class ImageOutputImage(models.Model):
    image_output_image_ID = models.AutoField(primary_key=True)
    report_ID = models.ForeignKey('Reports', on_delete=models.SET_NULL, null=True)
    image_output_filename = models.CharField(max_length=200, null=True)
    # Source image
    source_image_filename = models.CharField(max_length=200, null=True)
    student = models.ForeignKey('Student', on_delete=models.SET_NULL, null=True)
    image = models.ForeignKey('Images', on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.image_output_filename
    

    