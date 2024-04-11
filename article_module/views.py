from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import ListView, DetailView
from article_module.models import Article, ArticleCategory, ArticleComment
from jalali_date import datetime2jalali, date2jalali


# Create your views here.

class ArticlesView(ListView):
    template_name = 'article_module/articles_page.html'
    model = Article
    context_object_name = 'articles'

    paginate_by = 3

    # برای فرستادن اطلاعات اضافه تز به صفحه :
    def get_context_data(self, *args, **kwargs):
        context = super(ArticlesView, self).get_context_data(*args, **kwargs)
        # context['date'] = date2jalali(self.request.user.date_joined)  => این لاین تاریخ عضویت اکانتی که درحال بازکردن صفحه مقالات است را برمیگرداند.و اگر کاربر لاگین نکرده باشد ارور میدهد
        category_name = self.kwargs.get('category')
        if self.request.user.is_authenticated:
            context['date'] = date2jalali(self.request.user.date_joined)
        if category_name is not None:
            context['category'] = ArticleCategory.objects.filter(url_title=category_name).first()
        return context

    # برای فیلتر کردن دیتاها :
    def get_queryset(self):
        basequery = super(ArticlesView, self).get_queryset().filter(is_active=True)
        category_name = self.kwargs.get('category')
        if category_name is not None:
            basequery = basequery.filter(selected_categories__url_title__iexact=category_name)
        return basequery


class ArticleDetailView(DetailView):
    template_name = 'article_module/article_detail_page.html'
    model = Article

    def get_context_data(self, *args, **kwargs):
        data = super().get_context_data(**kwargs)
        # loaded_article = self.object
        loaded_article = kwargs.get('object')
        comments = ArticleComment.objects.filter(parent=None, article=loaded_article).prefetch_related(
            'articlecomment_set').order_by('-create_date')

        if Article.objects.filter(pk__lt=loaded_article.pk).last():
            previous_article = Article.objects.filter(pk__lt=loaded_article.pk, is_active=True).last()
        else:
            previous_article = None

        if Article.objects.filter(pk__gt=loaded_article.pk).first():
            next_article = Article.objects.filter(pk__gt=loaded_article.pk, is_active=True).first()
        else:
            next_article = None
        data['previous_article'] = previous_article
        data['next_article'] = next_article
        if loaded_article.is_active == True:
            data['comments'] = comments

            return data
        else:
            raise Http404


def article_categories_component(request):
    data = ArticleCategory.objects.prefetch_related('articlecategory_set').filter(is_active=True, parent=None)
    context = {
        'main_categories': data
    }
    return render(request, 'article_module/component/article_categories_component.html', context)


def add_article_comment(request: HttpRequest):
    # print(request.GET)
    if request.user.is_authenticated:
        # print(request.GET)
        article_id = request.GET.get('articleId')
        article_comment = request.GET.get('articleComment')
        if request.GET.get('parentId'):
            parent_id = request.GET.get('parentId')
        else:
            parent_id = None

        # print(article_id,article_comment,parent_id)

        new_comment = ArticleComment(article_id=article_id, text=article_comment, parent_id=parent_id,user=request.user)
        new_comment.save()

        # برای استفاده در فایل custom.js برای اینکه صفحه بدون رفرش شدن اپدیت شود
        comments = ArticleComment.objects.filter(parent=None, article=article_id).prefetch_related(
            'articlecomment_set').order_by('-create_date')
        article = Article.objects.filter(id=article_id).first()
        return render(request, 'article_module/component/article_comments_component.html',{"comments": comments, 'article': article})


def delete_article_comment(request):
    comment_id = request.GET.get('comment_id')
    article_id = request.GET.get('article_id')
    comment = ArticleComment.objects.filter(id=comment_id,user_id=request.user.id,article_id=article_id).first()
    print(comment)
    if comment is not None:
        comment.delete()
        comments = ArticleComment.objects.filter(parent=None, article_id=comment.article_id).prefetch_related('articlecomment_set').order_by('-create_date')
        article = Article.objects.filter(id=article_id).first()
        context = {"comments": comments, 'article': article, "request":request}
        data = render_to_string('article_module/component/article_comments_component.html', context)

        return JsonResponse({
            'status': 'success',
            'body': data,
            'text': 'کامنت مورد نظر با موفقیت حذف شد!',
            'icon': 'success',
            'confirm_button_text': 'باشه!'
        })
    else:
        return JsonResponse({
            'status': 'fail',
            'body': None,
            'text': 'حذف کامنت ناموفق بود!',
            'icon': 'error',
            'confirm_button_text': 'باشه!'
        })