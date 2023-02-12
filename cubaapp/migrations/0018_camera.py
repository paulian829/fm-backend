# Generated by Django 4.1.4 on 2023-02-12 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cubaapp', '0017_rename_date_created_nofacemaskimages_created'),
    ]

    operations = [
        migrations.CreateModel(
            name='Camera',
            fields=[
                ('camera_ID', models.AutoField(primary_key=True, serialize=False)),
                ('camera_name', models.CharField(max_length=200, null=True)),
                ('ip_address', models.CharField(max_length=200, null=True)),
                ('camera_details', models.CharField(max_length=200, null=True)),
                ('other_details', models.CharField(max_length=200, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('camera_status', models.CharField(max_length=200, null=True)),
            ],
        ),
    ]
