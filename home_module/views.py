from django.db.models import Count, Sum
from django.shortcuts import render
from django.views import View
from django.views.generic.base import TemplateView

from order_module.models import OrderDetail, Order
from product_module.models import Product, ProductCategory, ProductVisit
from utils.convertors import group_list
from site_module.models import SiteSetting, FooterLinkBox, Slider, SiteBanner


# Create your views here.

# with functions base view :

# def index_page(request):
#     return render(request, 'home_module/index_page.html')

# with class base view :
# By inheriting from the View class :


# class IndexPageView(View):
#     def get(self,request):
#         return render(request,"home_module/index_page.html")


# By inheriting from the TemplateView class :
class IndexPageView(TemplateView):
    template_name = "home_module/index_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['data']="this is data in home page"
        # context['message'] = "this is message in home page"
        # =-=-=-=-=-==-=-=-=-=-===-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-===-=-==-=-=-=-
        context['slider'] = Slider.objects.filter(is_active=True)
        # =-=-=-=-=-==-=-=-=-=-===-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-===-=-==-=-=-=-
        latest_products = Product.objects.filter(is_active=True, is_delete=False).order_by('-id')[:12]
        context['latest_products'] = group_list(latest_products, 4)
        # =-=-=-=-=-==-=-=-=-=-===-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-===-=-==-=-=-=-
        # dar Count be jaye productvisit_set bayad productvisit ro pass dad
        most_visit_products = Product.objects.annotate(visit_count=Count("productvisit")).filter(is_active=True,is_delete=False).order_by('-visit_count')[:12]
        context['most_visit_products'] = group_list(most_visit_products)
        # =-=-=-=-=-==-=-=-=-=-===-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-===-=-==-=-=-=-
        categories = list(ProductCategory.objects.filter(is_active=True, is_delete=False)[:6])
        categories_products = []
        for category in categories:
            item = {
                'id': category.id,
                'title': category.title,
                'products': list(category.product_categories.all()[:4])
            }
            categories_products.append(item)
        context['categories_products'] = categories_products
        # =-=-=-=-=-==-=-=-=-=-===-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-===-=-==-=-=-=-
        most_bought_products = Product.objects.filter(orderdetail__order__is_paid=True).annotate(order_count=Sum('orderdetail__count')).order_by('-order_count')[:12]
        context['most_bought_products'] = group_list(most_bought_products)
        return context


def site_header_component(request):
    setting = SiteSetting.objects.filter(is_main_setting=True).first()
    context = {
        'site_setting': setting
    }
    return render(request, 'shared/site_header_component.html', context)


def site_footer_component(request):
    setting = SiteSetting.objects.filter(is_main_setting=True).first()
    footer_link_boxes = FooterLinkBox.objects.all()
    context = {
        'site_setting': setting,
        'footer_link_boxes': footer_link_boxes
    }
    return render(request, 'shared/site_footer_component.html', context)


class AboutView(TemplateView):
    template_name = 'home_module/about_page.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        site_setting = SiteSetting.objects.filter(is_main_setting=True).first()
        context['site_setting'] = site_setting

        return context


class VipProducts(TemplateView):
    template_name = 'home_module/vip-products.html'
    def get_context_data(self, *args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['date'] = self.request.user.date_joined