# Generated by Django 4.1.1 on 2023-04-25 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SiteSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(max_length=200, verbose_name='نام سایت')),
                ('site_url', models.CharField(max_length=200, verbose_name='دامنه سایت')),
                ('about_us_text', models.TextField(verbose_name='متن درباره ما سایت')),
                ('address', models.CharField(max_length=200, verbose_name='آدرس سایت')),
                ('phone', models.CharField(blank=True, max_length=200, null=True, verbose_name='تلفن سایت')),
                ('fax', models.CharField(blank=True, max_length=200, null=True, verbose_name='فکس سایت')),
                ('email', models.CharField(blank=True, max_length=200, null=True, verbose_name='ایمیل سایت')),
                ('copy_right', models.TextField(max_length=200, verbose_name='متن کپی رایت سایت سایت')),
                ('site_logo', models.ImageField(upload_to='images/site-setting', verbose_name='لوگوی سایت')),
                ('is_main_setting', models.BooleanField(verbose_name='تنظیمات اصلی')),
            ],
            options={
                'verbose_name': 'تنظیمات سایت',
                'verbose_name_plural': 'تنظیمات',
            },
        ),
    ]
