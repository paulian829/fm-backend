# Generated by Django 4.1.4 on 2023-02-12 11:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cubaapp', '0018_camera'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='camera',
            name='camera_status',
        ),
        migrations.AddField(
            model_name='camera',
            name='enabled',
            field=models.BooleanField(default=True),
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=200, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('face_recognition', models.CharField(max_length=200, null=True)),
                ('false_alarm', models.BooleanField(default=False)),
                ('source_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cubaapp.camera')),
            ],
        ),
    ]