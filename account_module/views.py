from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.views import View
from django.views.generic import CreateView

from .forms import RegisterForm, LoginForm, ForgetPassForm, ResetPasswordForm
from .models import User
from django.utils.crypto import get_random_string
from django.contrib.auth import login, logout
from utils.email_service import send_email


# Create your views here.

# user = get_user_model()

class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        context = {
            'register_form': register_form
        }
        return render(request, 'account_module/register.html', context)

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_email = register_form.cleaned_data.get('email')
            user_password = register_form.cleaned_data.get('password')
            new_user = User(email=user_email, email_active_code=get_random_string(72), username=user_email, is_active=0)
            new_user.set_password(user_password)
            new_user.save()
            # todo: send email active code
            send_email('فعالسازی حساب کاربری', new_user.email, {'user': new_user}, 'emails/activate_account.html')
            return redirect('login_page')

        context = {
            'register_form': register_form
        }
        return render(request, 'account_module/register.html', context)


class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        return render(request, 'account_module/login.html', context={'login_form': login_form})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_email = login_form.cleaned_data.get('email')
            user_password = login_form.cleaned_data.get('password')
            user = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                if not user.is_active:
                    login_form.add_error('email', 'حساب کاربری شما فعال نشده است')
                else:
                    is_password_correct: bool = user.check_password(user_password)
                    if is_password_correct:
                        next = request.POST.get('next')
                        login(request, user)
                        if next is not None:
                            return redirect(next)
                        return redirect('user_panel_dashboard')
                    else:
                        login_form.add_error('email', 'کلمه عبور اشتباه است')
            else:
                login_form.add_error('email', 'کاربری با مشخصات وارد شده یافت نشد')
        return render(request, 'account_module/login.html', context={'login_form': login_form})


class ActivateAccountView(View):
    def get(self, request, email_active_code):
        user = User.objects.filter(email_active_code__iexact=email_active_code).first()
        if user is not None:
            if not user.is_active:
                user.is_active = True
                user.email_active_code = get_random_string(72)
                user.save()
                # todo: show success message to user
                return redirect('login_page')

            else:
                # todo: show your account was activated message to user
                pass
        raise Http404


class ForgetPasswordView(View):
    def get(self, request):
        return render(request, 'account_module/forgot_password.html', {'forget_pass_form': ForgetPassForm})

    def post(self, request):
        forget_pass_form = ForgetPassForm(request.POST)

        if forget_pass_form.is_valid():
            user_email = forget_pass_form.cleaned_data.get('email')
            user: User = User.objects.filter(email__iexact=user_email).first()

            if user is not None:
                # todo: send email reset password
                send_email('بازیابی کلمه عبور', user_email, {'user': user}, 'emails/reset_password.html')
                pass

        return render(request, 'account_module/forgot_password.html', {'forget_pass_form': forget_pass_form})


class ResetPasswordView(View):
    def get(self, request, active_code):
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()

        if user is not None:
            reset_pass_form = ResetPasswordForm()
            return render(request, 'account_module/reset_password.html', {
                'reset_pass_form': reset_pass_form,
                'user': user
            })

    def post(self, request, active_code):
        reset_pass_form = ResetPasswordForm(request.POST)
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()
        if reset_pass_form.is_valid():
            if user is None:
                return redirect("login_page")
            else:
                user_password = reset_pass_form.cleaned_data.get("password")
                user.set_password(user_password)
                user.email_active_code = get_random_string(72)
                user.is_active = True
                user.save()
                return redirect('login_page')
        return render(request, 'account_module/reset_password.html',
                      context={"reset_pass_form": reset_pass_form, 'user': user})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login_page')
