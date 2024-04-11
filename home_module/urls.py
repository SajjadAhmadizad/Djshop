from django.urls import path, include
from . import views
urlpatterns=[
    # path('',views.index_page,name='home-page'),
    path('',views.IndexPageView.as_view(),name='home-page'),
    path('',include('account_module.urls')),
    path('product-list/',include('product_module.urls'),name='product-list'),
    # path('site-header',views.site_header_partial)
    path('about-us', views.AboutView.as_view(),name='about_page'),
    path('vip-products', views.VipProducts.as_view(),name='vip_products'),
]