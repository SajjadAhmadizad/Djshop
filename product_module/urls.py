from django.urls import path
from . import views
urlpatterns=[
    # path('',views.product_list),
    path('',views.ProductListView.as_view(),name='product-list'),
    path('cat/<cat>',views.ProductListView.as_view(),name='product-categories-list'),
    path('brand/<brand>',views.ProductListView.as_view(),name='product-brands-list'),
    # path('product-list/',views.product_list),
    # path('<slug:slug>',views.product_detail,name='product-detail'),
    path('product-favorite/', views.AddProductFavorite.as_view(), name='product-favorite'),
    path('remove-product-favorite/', views.RemoveProductFavorite.as_view(), name='remove-product-favorite'),
    path('<slug:slug>', views.ProductDetailView.as_view(), name='product-detail'),
    path('add-product-comment/', views.AddProductComment,name="add-product-comment")
]