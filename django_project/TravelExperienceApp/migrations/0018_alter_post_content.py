# Generated by Django 3.2.5 on 2021-08-10 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TravelExperienceApp', '0017_alter_post_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
