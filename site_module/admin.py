from django.contrib import admin
from .models import SiteSetting, FooterLinkBox, FooterLink, Slider, SiteBanner


# Register your models here.

class FooterLinkAdmin(admin.ModelAdmin):
    list_display = ['title','url']

class SliderAdmin(admin.ModelAdmin):
    list_display = ['title','url','is_active']
    list_filter = ['title','url','is_active']
    list_editable = ['url','is_active']

class SiteBannerAdmin(admin.ModelAdmin):
    list_display = ['title','url','position']


admin.site.register(SiteSetting)
admin.site.register(FooterLinkBox)
admin.site.register(Slider,SliderAdmin)
admin.site.register(FooterLink,FooterLinkAdmin)
admin.site.register(SiteBanner,SiteBannerAdmin)
