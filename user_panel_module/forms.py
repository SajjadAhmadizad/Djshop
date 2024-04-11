from django import forms
from django.core.exceptions import ValidationError

from account_module.models import User


class EditProfileModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'avatar', 'address', 'about_user']
        # fields='__all__'
        # exclude=['response'] # all except response
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام'
            }, ),
            'last_name': forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "نام خانوادگی"
            }),
            'avatar': forms.FileInput(attrs={
                "class": "form-control",
                "placeholder": "تصویر آواتار"
            }),
            'address': forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "آدرس",
                "rows": 3,
                "id": "message"
            }),
            'about_user': forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "درباره کاربر",
                "rows": 6,
                "id": "message"
            }),
        }
        labels = {
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'avatar': 'تصویر آواتار',
            'address': 'آدرس',
            'about_user': 'درباره کاربر'
        }

    def clean_first_name(self):
        name = self.cleaned_data.get('first_name')

        if name is not None and name != '':
            return name
        else:
            raise ValidationError("نام خود را وارد کنید!")

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')

        if last_name is not None and last_name != '':
            return last_name
        else:
            raise ValidationError("نام خانوادگی خود را وارد کنید!")


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class':'form-control'
            }
        ),
        label='کلمه عبور فعلی'
    )
    new_password = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class':'form-control'
            }
        ),
        label="کلمه عبور جدید"
    )
    confirm_password = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class':'form-control'
            }
        ),
        label='تکرار کلمه عبور جدید'
    )

    def clean_password(self):
        new_password = self.cleaned_data.get('new_password')
        if len(new_password) > 4:
            if new_password.isdigit() == False:
                return new_password
            else:
                raise ValidationError("رمز عبور نمی‌تواند تنها شامل اعداد باشد")
        else:
            raise ValidationError("طول کلمه عبور بسیار کوتاه است(حداقل 5 کلمه)")

    def clean_confirm_password(self):
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if confirm_password == new_password:
            return confirm_password
        else:
            raise ValidationError("کلمه عبور وارد شده با تکرار آن مطابقت ندارد!")
