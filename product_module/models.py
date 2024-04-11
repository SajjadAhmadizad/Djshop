from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.utils.text import slugify

from account_module.models import User


# Create your models here.


class ProductCategory(models.Model):
    title = models.CharField(max_length=33, db_index=True, verbose_name="عنوان")
    url_title = models.CharField(max_length=300, db_index=True, verbose_name='عنوان در url')
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال')
    is_delete = models.BooleanField(verbose_name='حذف شده / حذف نشده')

    def __str__(self):
        return f"({self.title} - {self.url_title})"

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


class ProductBrand(models.Model):
    title = models.CharField(max_length=100, db_index=True, verbose_name='نام برند')
    url_title = models.CharField(max_length=200, verbose_name='نام در url', db_index=True)
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال')

    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برندها'

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=300, verbose_name='عنوان')

    category = models.ManyToManyField(
        ProductCategory,
        related_name='product_categories',
        verbose_name='دسته بندی ها')
    image = models.ImageField(upload_to='images/products', null=True, blank=True, verbose_name='تصویر محصول')
    brand = models.ForeignKey(ProductBrand, verbose_name='برند', on_delete=models.CASCADE, null=True, blank=True)
    price = models.IntegerField(verbose_name="قیمت")
    short_description = models.CharField(max_length=360, null=True, db_index=True, verbose_name='توضیحات کوتاه')
    description = models.TextField(db_index=True, verbose_name='توضیحات اصلی')
    slug = models.SlugField(null=False, max_length=200, blank=True,
                            unique=True)  # ,editable=False) #vaghti blank=True ast , an field mitavanad dar admin khali bashad vagarna error midahad
    # vaghti editable=True digar an field dar admin ghabel virayesh nist va digar neshan dade nemishavad
    # vaghti unique = True  => agar an field tekrari bashad az zakhire an jologiri mikonad
    # db_index besorate pishfarz baraye SlugField barabare True ast
    is_active = models.BooleanField(default=False, verbose_name='فعال/غیرفعال')
    is_delete = models.BooleanField(verbose_name='حذف شده / حذف نشده')

    def __str__(self):
        return f"{self.title} ({self.price})  (({self.slug}))"

    def get_absolute_url(self):
        return reverse('product-detail', args=[self.slug])

    def save(self, *args, **kwargs):
        # self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'


class ProductTag(models.Model):
    caption = models.CharField(max_length=300, db_index=True, verbose_name="عنوان")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_tags')
    is_delete = models.BooleanField(verbose_name='حذف شده / حذف نشده')

    class Meta:
        verbose_name = 'تگ محصول'
        verbose_name_plural = 'تگ های محصولات'

    def __str__(self):
        return self.caption


class ProductVisit(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    ip = models.CharField(max_length=30, verbose_name='آی پی کاربر')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, verbose_name='کاربر')

    def __str__(self):
        return f"{self.product.title} / {self.ip}"

    class Meta:
        verbose_name='بازدید محصول'
        verbose_name_plural = 'بازدیدهای محصول'


class ProductGallery(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='محصول')
    image = models.ImageField(upload_to='images/product-gallery', verbose_name='تصویر')

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'تصویر گالری'
        verbose_name_plural = 'گالری تصاویر'


class ProductComment(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name='محصول')
    text = models.TextField(verbose_name='متن کامنت')
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='کاربر')
    create_date = models.DateTimeField(auto_now_add=True,verbose_name='تاریخ ثبت')

    class Meta:
        verbose_name = 'نظر محصول'
        verbose_name_plural = 'نظرات محصول'

    def __str__(self):
        if self.user.get_full_name():
            return self.user.get_full_name()
        return self.user.email
