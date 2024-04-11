from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from .models import User


class RegisterForm(forms.Form):
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(),
        # validators=[validators.MaxValueValidator(70),validators.EmailValidator],
        error_messages={'required':'فیلد ایمیل حتما باید پر شود!'}
    )
    password = forms.CharField(
        label='کلمه عبور',
        widget=forms.PasswordInput()
    )
    confirm_password = forms.CharField(
        label='تکرار کلمه عبور',
        widget=forms.PasswordInput()
    )

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) > 4 :
            if password.isdigit() == False:
                return password
            else:
                raise ValidationError("رمز عبور نمی‌تواند تنها شامل اعداد باشد")
        else:
            raise ValidationError("طول کلمه عبور بسیار کوتاه است(حداقل 5 کلمه)")

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password == confirm_password:
            return password
        else:
            raise ValidationError('کلمه عبور با تکرار کلمه عبور مغایرت دارد')


    def clean_email(self):
        email = self.cleaned_data.get('email')

        user = User.objects.filter(email__iexact=email).exists()
        if user:
            raise ValidationError('ایمیل وارد شده تکراری است(از فرم)')
        else:
            if '@yahoo' in email:
                raise ValidationError("امکان ثبت نام با ایمیل یاهو وجود ندارد!")
            else:
                return email

class LoginForm(forms.Form):
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={'placeholder':"ایمیل"}),
        error_messages={'required':'فیلد ایمیل حتما باید پر شود!'}
    )
    password = forms.CharField(
        label='کلمه عبور',
        widget=forms.PasswordInput(attrs={'placeholder':"کلمه عبور"})
    )


class ForgetPassForm(forms.Form):
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs = {'placeholder':'ایمیل'},),
        # validators=[validators.MaxValueValidator(70),validators.EmailValidator],
        error_messages={'required':'فیلد ایمیل حتما باید پر شود!'}
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        is_exist = User.objects.filter(email__iexact=email).first()
        user:User = User.objects.filter(email__iexact=email).first()

        if "@yahoo" in email:
            raise ValidationError("امکان ثبت نام در سایت با ایمیل یاهو وجود ندارد")
        else:
            if not is_exist:
                raise ValidationError("ایمیلی با این آدرس تا کنون در سایت ثبت نام نکرده است!")
            else:
                if not user.is_active:
                    raise ValidationError("حساب کاربری موردنظر فعال نمیباشد!")
                else:
                    return email


class ResetPasswordForm(forms.Form):
    password = forms.CharField(
        label='کلمه عبور',
        widget=forms.PasswordInput()
    )
    confirm_password = forms.CharField(
        label='تکرار کلمه عبور',
        widget=forms.PasswordInput()
    )

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) > 4:
            if password.isdigit() == False:
                return password
            else:
                raise ValidationError("رمز عبور نمی‌تواند تنها شامل اعداد باشد")
        else:
            raise ValidationError("طول کلمه عبور بسیار کوتاه است(حداقل 5 کلمه)")

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password == confirm_password:
            return password
        else:
            raise ValidationError('کلمه عبور با تکرار کلمه عبور مغایرت دارد')
