from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from coreapp.forms import CommentForm, SignupForm, MessageForm
from coreapp.models import User, Category, Article, Comment, Trending, Featured, Tag, Message, FAQ
from hitcount.views import HitCountDetailView
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
class SignupView(generic.CreateView):
    model = User
    form_class = SignupForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('HomeView')


class HomeView(generic.TemplateView):
    template_name = 'frontend/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        categories = Category.objects.annotate(Count('article'))
        hot_categories = categories.values_list('title', 'slug', 'article__count')
        context['hot_categories'] = hot_categories
        context['categories'] = Category.objects.all().filter(is_active=True)
        context['tags'] = Tag.objects.all()
        context['trending'] = Trending.objects.all().order_by('-updated_at').filter(is_active=True)[:5]
        context['featured'] = Featured.objects.all().order_by('-updated_at').filter(is_active=True)[:5]
        latest_article = Article.objects.all().order_by('-updated_at').filter(is_published=True)[:15]
        context['latest_article'] = latest_article
        context['articles'] = latest_article[5:]
        context['politics'] = Article.objects.all().order_by('-updated_at').filter(is_published=True).filter(
            category=3)[:5]
        context['sports'] = Article.objects.all().order_by('-updated_at').filter(is_published=True).filter(category=9)[
                            :5]
        return context


class ArticleListView(generic.ListView):
    model = Article
    context_object_name = 'articles'
    paginate_by = 15
    slug_url_kwarg = 'slug'
    query_pk_and_slug = True
    template_name = "frontend/article_list.html"

    def get_queryset(self):
        return Article.objects.filter(category__slug=self.kwargs['slug'])


class ArticleListByTagView(generic.ListView):
    model = Article
    context_object_name = 'articles'
    paginate_by = 20
    slug_url_kwarg = 'name'
    query_pk_and_slug = True
    template_name = "frontend/article_list.html"

    def get_queryset(self):
        return Article.objects.filter(tag__name__contains=self.kwargs['name'])


class ArticleDetailView(HitCountDetailView):
    count_hit = True
    model = Article
    context_object_name = "article"
    slug_url_kwarg = 'article_slug'
    template_name = "frontend/article_detail.html"

    def get_object(self, **kwargs):
        return get_object_or_404(Article, slug=self.kwargs['article_slug'])

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        context['post_comments'] = Comment.objects.all().filter(article=self.get_object())
        context['comment_form'] = CommentForm
        return context


def add_comment(request, article_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            article = Article.objects.get(id=article_id)
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.article = article
                comment.save()
                return redirect(reverse('ArticleDetailView',
                                        kwargs={"category_slug": article.category.slug, "article_slug": article.slug}))

    else:
        return redirect("HomeView")


class ContactView(generic.CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'frontend/contact.html'
    success_url = reverse_lazy('ContactView')


class FAQListView(generic.ListView):
    model = FAQ
    template_name = 'frontend/faq.html'
    queryset = FAQ.objects.all()
    context_object_name = 'faqs'
