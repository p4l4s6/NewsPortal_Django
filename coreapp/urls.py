from django.urls import path
from coreapp import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='HomeView'),
    path('category/<int:category_id>/', views.ArticleListView.as_view(), name='ArticleListView'),
    path('article/<slug:slug>/', views.ArticleDetailView.as_view(), name='ArticleDetailView'),
]
