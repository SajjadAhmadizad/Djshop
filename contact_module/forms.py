from django import forms
from django.core.exceptions import ValidationError

from .models import ContactUs
class ContactUsForm(forms.Form):
    full_name = forms.CharField(label='نام و نام خانوادگی',
                                widget=forms.TextInput(attrs={
                                    "class":"form-control",
                                    "placeholder":"نام و نام خانوادگی"
                                }),
                                required=True,
                                max_length=50,
                                error_messages={
                                    'max_length':'نام و نام خانوادگی نمی تواند بیشتر از ۵۰ کاراکتر باشد!',
                                    'required':'لطفا نام و نام خانوادگی را وارد کنید'
                                })
    email = forms.EmailField(label='ایمیل',
                             widget=forms.EmailInput(attrs={
                                 "class": "form-control",
                                 "placeholder": "ایمیل"
                             }),
                             required=True,
                             error_messages={
                                 'required':'لطفا ایمیل را وارد کنید'
                             })
    subject = forms.CharField(label='عنوان',
                              widget=forms.TextInput(attrs={
                                  "class": "form-control",
                                  "placeholder": "عنوان"
                              }),
                            required = True,
                            error_messages = {
                                'required': 'لطفا عنوان را وارد کنید'
                            })
    text = forms.CharField(label='متن پیام',
                           required = True,
                           widget=forms.Textarea(attrs={
                               'class':"form-control",
                               "placeholder":"متن پیام",
                               "id":"message"
                           }),
                           error_messages = {
                               'required': 'لطفا متن پیام را وارد کنید',
                           })

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if "@yahoo.com" in email:
            raise ValidationError("استفاده از ایمیل @yahoo.com مجاز نیست!")
        else:
            return email


class ContactUsModelForm(forms.ModelForm):
    class Meta:
        model=ContactUs
        fields=['full_name','email','title','message']
        # fields='__all__'
        # exclude=['response'] # all except response
        widgets={
            'full_name': forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'نام و نام خانوادگی'
            },),
            'email' : forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "ایمیل"
            }),
            'title' : forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "عنوان"
            }),
            'message' : forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "متن پیام",
                "rows":5,
                "id":"message"
            }),
        }
        labels = {
            'full_name':'نام و نام خانوادگی شما',
            'email':'ایمیل شما'
        }
        error_messages={
            "email":{
                "required":"ایمیل خود را وارد کنید",
                "invalid":"ساختار ایمیل وارد شده نادرست است!"
            },
            "full_name":{
                "required":"نام و نام خانوادگی خود را وارد کنید",
                "max_length":"postkeleft"
            }
        }

class ProfileForm(forms.Form):
    user_image = forms.FileField(label='تصویر ارسالی کاربر')
