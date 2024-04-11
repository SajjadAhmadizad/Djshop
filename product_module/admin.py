from django.contrib import admin
from . import models


# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'is_active', 'is_delete', 'brand']
    list_filter = ['category', 'is_active']
    list_editable = ['price', 'is_active', 'is_delete']

class ProductCommentAdmin(admin.ModelAdmin):
        list_display = ['user', 'text', 'create_date']
        list_filter = ['user']


admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductCategory)
admin.site.register(models.ProductTag)
admin.site.register(models.ProductBrand)
admin.site.register(models.ProductVisit)
admin.site.register(models.ProductGallery)
admin.site.register(models.ProductComment,ProductCommentAdmin)
