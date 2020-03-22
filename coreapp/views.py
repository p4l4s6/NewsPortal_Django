from django.shortcuts import render
from django.views import generic
from coreapp.models import Category, Article, Comment, Trending, Featured
from hitcount.views import HitCountDetailView


# Create your views here.
class HomeView(generic.TemplateView):
    template_name = 'frontend/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['trending'] = Trending.objects.all().order_by('-updated_at').filter(is_active=True)[:5]
        context['featured'] = Featured.objects.all().order_by('-updated_at').filter(is_active=True)[:5]
        context['articles'] = Article.objects.all().order_by('-updated_at').filter(is_published=True)
        context['politics'] = Article.objects.all().order_by('-updated_at').filter(is_published=True).filter(
            category=3)[:5]
        context['sports'] = Article.objects.all().order_by('-updated_at').filter(is_published=True).filter(category=9)[
                            :5]
        return context


class ArticleListView(generic.ListView):
    model = Article
    context_object_name = 'articles'
    paginate_by = 20
    template_name = "frontend/article_list.html"

    def get_queryset(self):
        return Article.objects.filter(category=self.kwargs['category_id'])


class ArticleDetailView(HitCountDetailView):
    count_hit = True
    model = Article
    context_object_name = "article"
    pk_url_kwarg = 'article_id'
    slug_url_kwarg = 'slug'
    query_pk_and_slug = True
    template_name = "frontend/article_detail.html"
