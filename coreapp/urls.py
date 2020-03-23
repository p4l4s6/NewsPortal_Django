from django.urls import path
from coreapp import views

urlpatterns = [
    path('comment/add/<int:article_id>/', views.add_comment, name='AddCommentView'),
    path('contact/', views.ContactView.as_view(), name='ContactView'),
    path('faq/', views.FAQListView.as_view(), name='FaqView'),
    path('', views.HomeView.as_view(), name='HomeView'),
    path('<slug:slug>/', views.ArticleListView.as_view(), name='ArticleListView'),
    path('tag/<str:name>/', views.ArticleListByTagView.as_view(), name='ArticleListByTagView'),
    path('<slug:category_slug>/<slug:article_slug>/', views.ArticleDetailView.as_view(), name='ArticleDetailView'),

]
