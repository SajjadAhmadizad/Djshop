from django.contrib import admin
from django.http import HttpRequest
from django.shortcuts import redirect

from . import models
from .models import Article


# Register your models here.

class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ['title','url_title','parent','is_active']
    list_editable = ['url_title', 'is_active','parent']

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title','slug','is_active','author']
    list_editable = ['is_active']

    def save_model(self, request:HttpRequest, obj:Article, form, change):
        print('change : ',change)
        print('request : ', request)
        print('user : ', request.user.email)
        # print('object : ', obj.slug)
        if not change:
            obj.author = request.user
        return super().save_model(request,obj,form,change)


class ArticleCommentAdmin(admin.ModelAdmin):
    list_display = ['user','create_date','parent']

admin.site.register(models.ArticleCategory,ArticleCategoryAdmin)
admin.site.register(models.Article,ArticleAdmin)
admin.site.register(models.ArticleComment,ArticleCommentAdmin)
