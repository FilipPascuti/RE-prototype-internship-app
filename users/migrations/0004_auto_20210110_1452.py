# Generated by Django 2.2.5 on 2021-01-10 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20210110_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='cv',
            field=models.FileField(blank=True, null=True, upload_to='media/students/cvs'),
        ),
        migrations.AlterField(
            model_name='student',
            name='profile_photo',
            field=models.ImageField(blank=True, null=True, upload_to='media/students/photos'),
        ),
    ]
