# Generated by Django 4.1.1 on 2023-02-17 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact_module', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactus',
            name='is_read_by_admin',
            field=models.BooleanField(default=False, verbose_name='خوانده شده توسط ادمین'),
        ),
    ]
