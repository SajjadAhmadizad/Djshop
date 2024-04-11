from django.shortcuts import render, get_object_or_404, redirect
from product_module.models import Product, ProductCategory, ProductBrand, ProductVisit, ProductGallery, ProductComment
from django.views.generic.base import TemplateView, View
from django.views.generic import ListView, DetailView
from django.http import Http404, HttpResponse, HttpRequest
from django.db.models import Avg, Min, Max, Count
from utils.http_service import get_client_ip
from utils.convertors import group_list
from site_module.models import SiteBanner


# Create your views here.

# with class base view:
# By inheriting from the TemplateView class

# class ProductListView(TemplateView):
#     template_name = "product_module/product_list.html"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         products = Product.objects.all().order_by('-price')
#         # number_of_product = products.count()
#         categories = ProductCategory.objects.all()
#         brands = ProductBrand.objects.all()
#
#         context['data'] = products
#         context['categories'] = categories
#         context['brands'] = brands
#
#         return context

# By inheriting from the TemplateView class :

# class ProductDetailView(TemplateView):
#     template_name = 'product_module/product_detail.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         slug = kwargs['slug']
#         product = get_object_or_404(Product, slug=slug)
#         brands = ProductBrand.objects.all()
#         categories = ProductCategory.objects.all()
#         context['product'] = product
#         context['brands'] = brands
#         context['categories'] = categories
#         return context

# By inheriting from the TemplateView class :

class ProductDetailView(DetailView):
    template_name = 'product_module/product_detail.html'
    model = Product

    def get_context_data(self, **kwargs):
        # =-=-=-=-=-==-=-=-=-=-===-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-===-=-==-=-=-=-
        context = super().get_context_data(**kwargs)
        loaded_product = self.object
        request = self.request
        # favorite_product_id = loaded_product.id == str(request.session.get('product_favorite'))
        if request.session.get("product_favorite"):
            if loaded_product.id in request.session.get("product_favorite"):
                context["is_favorite"] = True
            else:
                context["is_favorite"] = False
        # =-=-=-=-=-==-=-=-=-=-===-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-===-=-==-=-=-=-
        banners = SiteBanner.objects.filter(is_active=True,position__iexact=SiteBanner.SiteBannerPosition.product_detail)
        context['banners'] = banners
        # =-=-=-=-=-==-=-=-=-=-===-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-===-=-==-=-=-=-
        user_ip = get_client_ip(request=self.request)
        user_id = None
        if self.request.user.is_authenticated:
            user_id = self.request.user.id
        has_been_visited = ProductVisit.objects.filter(ip__iexact=user_ip, product_id=loaded_product.id).exists()
        if not has_been_visited:
            new_visit = ProductVisit(ip=user_ip, product=loaded_product, user_id=user_id)
            new_visit.save()
        # =-=-=-=-=-==-=-=-=-=-===-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-===-=-==-=-=-=-
        galleries = list(ProductGallery.objects.filter(product_id=loaded_product.id).all())
        galleries.insert(0, loaded_product)
        galleries = group_list(galleries, 3)
        context['product_galleries_group'] = galleries
        # =-=-=-=-=-==-=-=-=-=-===-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-===-=-==-=-=-=-
        related_products = list(Product.objects.filter(is_active=True, is_delete=False, brand_id=loaded_product.brand_id).exclude(pk=loaded_product.id).all())
        related_products = group_list(related_products,3)
        context['related_products'] = related_products
        # =-=-=-=-=-==-=-=-=-=-===-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-===-=-==-=-=-=-
        comments = ProductComment.objects.filter(product_id=loaded_product.id).all().order_by('-create_date')
        context['comments'] = comments
        context['comment_count'] = comments.count()
        return context



class AddProductFavorite(View):
    def post(self, request):
        product_id = request.POST['product_id']
        product = Product.objects.get(pk=product_id)

        # save in session :
        favorite_list = request.session.get("product_favorite", [])  # اگر در سشن این کلید وجود داشته باشد
        # مقدار فیوریت لیست برابر مقدار ولیوی این کلید میشود
        # در غیر اینصورت مقدار فیوریت لیست برابر یک لیست خالی میشود

        if int(product_id) not in favorite_list:
            favorite_list.append(int(product_id))
        request.session["product_favorite"] = favorite_list
        # format session JSON(ye chizi shabihe dictionary) hast va nemishe ye object az
        # class product ro tosh rikht pas id ro mirizim
        return redirect(product.get_absolute_url())


class RemoveProductFavorite(View):
    def post(self, request):
        product_id = request.POST['product_id']
        product = Product.objects.get(pk=product_id)

        # remove from session :

        request.session["product_favorite"].remove(int(product_id))
        request.session.save()

        return redirect(product.get_absolute_url())


# By inheriting from the ListView class

class ProductListView(ListView):
    template_name = 'product_module/product_list.html'
    model = Product
    context_object_name = 'products'
    ordering = ['price']
    paginate_by = 3

    # baraye ferestadane min va max price be safhe product list baraye taeein baze filter gheymat
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        # query = self.get_queryset()
        # product: Product = query.order_by('-price').first()

        product: Product = Product.objects.order_by('-price').first()

        db_max_price = product.price if product is not None else 1000000
        context['db_max_price'] = db_max_price
        context['start_price'] = request.GET.get('start_price') or 0
        context['end_price'] = request.GET.get('end_price') or db_max_price

        banners = SiteBanner.objects.filter(is_active=True, position__iexact=SiteBanner.SiteBannerPosition.product_list)
        context['banners'] = banners
        return context

    def get_queryset(self):
        base_query = super(ProductListView, self).get_queryset()
        data = base_query.filter(is_active=True)
        # return data.order_by('-price')
        category_name = self.kwargs.get('cat')
        brand_name = self.kwargs.get('brand')
        request = self.request

        start_price = request.GET.get('start_price')
        end_price = request.GET.get('end_price')

        if start_price is not None:
            data = data.filter(price__gte=start_price)

        if end_price is not None:
            data = data.filter(price__lte=end_price)

        if category_name is not None:
            data = data.filter(
                category__url_title__iexact=category_name)  # exact be bozorg va kochaki horof hassas ast amma iexact na

        if brand_name is not None:
            data = data.filter(brand__url_title__iexact=brand_name)

        return data


def AddProductComment(request:HttpRequest):
    if request.method=="POST":
        if request.user.is_authenticated:
            comment = request.POST.get('productComment')
            productId = request.POST.get('product_id')
            product = Product.objects.filter(pk=productId, is_delete=False, is_active=True).first()
            new_comment = ProductComment(product_id=productId,text=comment,user_id=request.user.id)
            new_comment.save()
            comments = ProductComment.objects.filter(product_id=productId).order_by('-create_date')
            return render(request,'includes/product_comment_partial.html',{'product':product,'comments':comments,"cpmment_count":comments.count()})


# with function base view :

# def product_list(request):
#
#     products = Product.objects.all().order_by('-price')
#     # number_of_product = products.count()
#     categories = ProductCategory.objects.all()
#     brands = ProductBrand.objects.all()
#     return render(request,'product_module/product_list.html',context={
#         'data':products,
#         'categories':categories,
#         'brands':brands,
#         # 'total_number_of_product':number_of_product
#     })

# def product_detail(request,slug):
#     product = get_object_or_404(Product,slug=slug)
#     brands = ProductBrand.objects.all()
#     categories = ProductCategory.objects.all()
#     return render(request,'product_module/product_detail.html',{'product':product,'brands':brands,'categories':categories})


def product_categories_component(request):
    categories = ProductCategory.objects.filter(is_active=True)
    return render(request, 'product_module/components/product_categories_component.html', {'categories': categories})


def product_brands_component(request):
    product_brands = ProductBrand.objects.annotate(products_count=Count('product')).filter(is_active=True)
    return render(request, 'product_module/components/product_brands_component.html',
                  {'product_brands': product_brands})
