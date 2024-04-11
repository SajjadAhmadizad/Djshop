from django.contrib import admin
from . import models
from utils.email_service import send_email

# Register your models here.

class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['title','email']

    def save_model(self, request, obj:models.ContactUs, form, change):
        if change and obj.is_read_by_admin == 1 and not obj.response:
            send_email('تماس با ما',obj.email,{'user':None},'emails/contact-us.html')
        elif change and obj.is_read_by_admin == 1 and obj.response:
            send_email('تماس با ما',obj.email,{'answer':obj.response},'emails/contact-us-message.html')

        return super().save_model(request, obj, form, change)


admin.site.register(models.ContactUs,ContactUsAdmin)
admin.site.register(models.UserProfile)