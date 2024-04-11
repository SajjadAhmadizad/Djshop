from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from order_module.models import Order, OrderDetail
from product_module.models import Product

# Create your views here.

def add_product_to_order(request: HttpRequest):
    product_id = int(request.GET.get("product_id"))
    count = int(request.GET.get("count"))

    if count < 1:
        # count = 1
        return JsonResponse({
            'status': 'success',
            'text': 'مقدار وارد شده صحیح نمیباشد!',
            'icon': 'error',
            'confirm_button_text': 'باشه ممنون!'
        })

    product: Product = Product.objects.filter(is_active=True, is_delete=False, pk=product_id).first()
    if request.user.is_authenticated:

        if product is not None:
            # current_order = Order.objects.filter(user_id=request.user.id,is_paid=False).first()
            current_order, created = Order.objects.get_or_create(user_id=request.user.id, is_paid=False)
            current_order_detail = current_order.orderdetail_set.filter(product_id=product_id).first()
            if current_order_detail is not None:
                current_order_detail.count += count
                current_order_detail.save()
            else:
                new_detail = OrderDetail(order_id=current_order.id, product_id=product_id, count=count)
                new_detail.save()
            return JsonResponse({
                'status': 'success',
                'text': 'محصول مورد نظر با موفقیت به سبد خرید اضافه شد!',
                'icon': 'success',
                'confirm_button_text': 'باشه ممنون!'
            })
        else:
            return JsonResponse({
                'status': 'not_found',
                'text': 'محصول مورد نظر یافت نشد!',
                'icon': 'error',
                'confirm_button_text': 'باشه ممنون!'
            })
    else:
        return JsonResponse({
            'status': 'not_auth',
            'icon': 'warning',
            'url': product.get_absolute_url(),
            'text': 'برای افزودن محصول به سبد خرید می بایست وارد سایت شوید!',
            'confirm_button_text': 'ورود به سایت'
        })
