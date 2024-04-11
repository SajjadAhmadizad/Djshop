from article_module.views import ArticlesView,ArticleDetailView,add_article_comment,delete_article_comment
from django.urls import path

urlpatterns = [
    path('',ArticlesView.as_view(),name = 'articles_list'),
    path('cat/<str:category>',ArticlesView.as_view(),name = 'articles_by_category_list'),
    # path('all-articles/<str:author>',ArticlesView.as_view(),name = 'article_by_user'),
    path('<slug>/',ArticleDetailView.as_view(),name = 'articles_detail'),
    path('add-article-comment',add_article_comment,name = 'add_article_comment'),
    path('delete-article-comment',delete_article_comment,name = 'delete_article_comment'),
]