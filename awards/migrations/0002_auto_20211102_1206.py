# Generated by Django 3.2.9 on 2021-11-02 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('awards', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_photo',
            field=models.ImageField(upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='project',
            name='image',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
