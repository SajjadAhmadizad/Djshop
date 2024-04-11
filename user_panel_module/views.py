from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import Http404, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import TemplateView, ListView
from order_module.models import Order, OrderDetail
from .forms import EditProfileModelForm, ChangePasswordForm
from account_module.models import User
from django.contrib.auth import logout
from django.utils.decorators import  method_decorator

# Create your views here.

@method_decorator(login_required, name='dispatch')
class UserPanelDashboardPage(TemplateView):
    template_name = 'user_panel_module/user_panel_dashboard_page.html'

@method_decorator(login_required, name='dispatch')
class EditUserProfilePage(View):
    def get(self, request):
        current_user = User.objects.filter(id=request.user.id).first()
        # edit_form = EditProfileModelForm(initial={
        #     'first_name':current_user.first_name,
        #     'last_name':current_user.last_name,
        #     'avatar':current_user.avatar,
        #     'address':current_user.address
        # })
        edit_form = EditProfileModelForm(instance=current_user)
        return render(request, 'user_panel_module/edit_profile_page.html',
                      {'form': edit_form, 'current_user': current_user})

    def post(self, request):
        current_user = User.objects.filter(id=request.user.id).first()
        edit_form = EditProfileModelForm(request.POST, request.FILES, instance=current_user)

        if edit_form.is_valid():
            edit_form.save(commit=True)
        return render(request, 'user_panel_module/edit_profile_page.html',
                      {'form': edit_form, 'current_user': current_user})

@method_decorator(login_required, name='dispatch')
class ChangePasswordPage(View):
    def get(self, request):
        if request.user.is_authenticated:
            change_password_form = ChangePasswordForm()
            return render(request, 'user_panel_module/change_password_page.html', {'form': change_password_form})
        else:
            raise Http404

    def post(self, request):
        if request.user.is_authenticated:
            change_password_form = ChangePasswordForm(request.POST)

            current_password = request.POST.get('current_password')
            current_user = User.objects.filter(id=request.user.id).first()
            is_password_correct: bool = current_user.check_password(current_password)

            if is_password_correct:
                if change_password_form.is_valid():
                    current_user: User = User.objects.filter(id=request.user.id).first()
                    current_user.set_password(request.POST.get("new_password"))
                    current_user.save()
                    logout(request)
                    return redirect('login_page')
            else:
                change_password_form.add_error('current_password', 'کلمه عبور وارد شده صحیح نمیباشد!')
            return render(request, 'user_panel_module/change_password_page.html', {'form': change_password_form})
        else:
            raise Http404


@method_decorator(login_required, name='dispatch')
class MyShopping(ListView):
    model = Order
    template_name = 'user_panel_module/user_shopping.html'

    def get_queryset(self):
        queryset=super().get_queryset()
        request=self.request
        queryset = queryset.filter(is_paid=True,user_id=request.user.id)
        return queryset


@login_required
def user_panel_menu_component(request):
    current_user = User.objects.filter(id=request.user.id).first()
    return render(request, 'user_panel_module/components/user_panel_menu_component.html',
                  {'current_user': current_user})

@login_required
def user_basket(request: HttpRequest):
    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(user_id=request.user.id,
                                                                                             is_paid=False)
    total_amount = 0
    for order_detail in current_order.orderdetail_set.all():
        total_amount += order_detail.product.price * order_detail.count
    context = {
        'order': current_order,
        'sum': total_amount
    }
    return render(request, 'user_panel_module/user_basket.html', context)

@login_required
def remove_order_detail(request: HttpRequest):
    detail_id = request.GET.get('detail_id')
    if detail_id is None:
        return JsonResponse({
            'status': 'not_found_detail_id',
            'body': 'null',
            'text': 'سبد خریدی یافت نشد!',
            'icon': 'error',
            'confirm_button_text': 'باشه ممنون!'
        })
    # current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(user_id=request.user.id,is_paid=False)
    # detail: OrderDetail = current_order.orderdetail_set.filter(id=detail_id).first()

    deleted_count, deleted_dict = OrderDetail.objects.filter(id=detail_id, order__user_id=request.user.id,
                                                             order__is_paid=False).delete()

    if deleted_count == 0:
        return JsonResponse({
            'status': 'detail_not_found',
            'body': 'null',
            'text': 'چنین سبد خریدی وجود ندارد!',
            'icon': 'error',
            'confirm_button_text': 'باشه ممنون!'
        })
    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(user_id=request.user.id,
                                                                                             is_paid=False)

    context = {
        'order': current_order,
        'sum': current_order.calculate_total_price()
    }
    return JsonResponse({
        'status': 'success',
        'body': render_to_string('user_panel_module/user_basket_content.html', context),
        'text': 'محصول مورد نظر با موفقیت از سبد خرید حذف شد!',
        'icon': 'success',
        'confirm_button_text': 'باشه ممنون!'
    })
    # return render(request, 'user_panel_module/user_basket_content.html', context)

@login_required
def change_order_detail_count(request: HttpRequest):
    detail_id = request.GET.get('detail_id')
    state = request.GET.get('state')

    if detail_id is None or state is None:
        return JsonResponse({
            'status': 'detail_or_state_not_found'
        })
    order_detail = OrderDetail.objects.filter(id=detail_id, order__is_paid=False,
                                              order__user_id=request.user.id).first()
    if state == 'increase':
        order_detail.count += 1
        order_detail.save()
    elif state == 'decrease':
        if order_detail.count == 1:
            order_detail.delete()
        else:
            order_detail.count -= 1
            order_detail.save()
    else:
        return JsonResponse({
            'status': 'state_invalid'
        })

    order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(user_id=request.user.id,is_paid=False)
    data = render_to_string('user_panel_module/user_basket_content.html',{'sum': order.calculate_total_price(), 'order': order})
    return JsonResponse({
        'status': 'success',
        'body': data
    })


def my_shopping_detail(request:HttpRequest ,order_id):
    order = Order.objects.prefetch_related('orderdetail_set').filter(id=order_id,user_id=request.user.id,is_paid=True).first()
    if order is None:
        raise Http404("سبد خرید مورد نظر یافت نشد")


    return render(request, 'user_panel_module/user_shopping_detail.html',{
        'order':order
    })