# Generated by Django 4.1.1 on 2023-04-16 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact_module', '0004_alter_userprofile_options_alter_userprofile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(upload_to='images', verbose_name='ارسال تصویر'),
        ),
    ]
