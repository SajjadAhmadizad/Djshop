from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    avatar = models.ImageField(upload_to='images/profile',verbose_name='تصویر آواتار',null=True,blank=True)
    email_active_code = models.CharField(max_length=100,verbose_name='کد فعالسازی ایمیل')
    about_user = models.TextField(null=True,blank=True,verbose_name='درباره شخص')
    address = models.TextField(null=True,blank=True,verbose_name='آدرس')
    is_vip = models.BooleanField(default=False,verbose_name='کاربر ویژه')

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        if self.get_full_name():
            return self.get_full_name()
        return self.email