# Generated by Django 3.2.5 on 2021-08-08 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TravelExperienceApp', '0015_auto_20210728_1821'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='image',
        ),
        migrations.AddField(
            model_name='post',
            name='file',
            field=models.FileField(default=1, upload_to='files'),
            preserve_default=False,
        ),
    ]
