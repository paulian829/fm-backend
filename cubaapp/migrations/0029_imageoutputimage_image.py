# Generated by Django 4.1.7 on 2023-03-04 10:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cubaapp', '0028_rename_image_output_image_filename_imageoutputimage_image_output_filename'),
    ]

    operations = [
        migrations.AddField(
            model_name='imageoutputimage',
            name='image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cubaapp.images'),
        ),
    ]
