# Generated by Django 4.1.7 on 2023-03-02 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cubaapp', '0022_remove_images_camera_source_id_images_path_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('student_ID', models.AutoField(primary_key=True, serialize=False)),
                ('student_name', models.CharField(max_length=200, null=True)),
                ('student_class', models.CharField(max_length=200, null=True)),
                ('student_section', models.CharField(max_length=200, null=True)),
                ('student_photo_filename', models.CharField(max_length=200, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]