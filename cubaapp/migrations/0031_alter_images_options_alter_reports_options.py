# Generated by Django 4.1.7 on 2023-04-07 09:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cubaapp', '0030_imageoutputimage_confidence'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='images',
            options={'verbose_name_plural': 'Images'},
        ),
        migrations.AlterModelOptions(
            name='reports',
            options={'verbose_name_plural': 'Reports'},
        ),
    ]
