# Generated by Django 4.1.3 on 2023-02-26 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cubaapp', '0020_reports_remove_images_face_recognition_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='reports',
            name='output_url',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
