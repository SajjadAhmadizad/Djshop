from django.db import models

# Create your models here.


class ContactUs(models.Model):
    title = models.CharField(max_length=300,verbose_name='عنوان')
    email = models.EmailField(max_length=300,verbose_name='ایمیل')
    full_name = models.CharField(max_length=300,verbose_name='نام و نام خانوادگی')
    message = models.TextField(verbose_name='متن تماس با ما')
    created_date = models.DateTimeField(verbose_name='تاریخ ایجاد',auto_now_add=True)  # vaghti auto_new_add=True  => agar yek nemone az in class sakhte
                                                                                        # shavad meghdar created_date be sorat khodkar barabare tarikhe an lahze mishavad
    response = models.TextField(verbose_name='متن پاسخ تماس با ما',null=True,blank=True)
    is_read_by_admin = models.BooleanField(verbose_name='خوانده شده توسط ادمین',default=False)

    class Meta:
        verbose_name= 'تماس با ما'
        verbose_name_plural = 'لیست تماس با ما'

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    # image = models.FileField(upload_to='images',verbose_name='تصویر آپلود شده')
    image = models.ImageField(upload_to='images',verbose_name='ارسال تصویر')


    def __str__(self):
        return self.image


    class Meta:
        verbose_name = 'تصویر آپلود شده'
        verbose_name_plural = 'لیست تصاویر آپلود شده'