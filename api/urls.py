from django.conf.urls import url
from rest_framework import routers

from .views import LoginView, SignUpView, UserViewSet, TagViewSet, CategoryViewSet, ArticleViewSet, CommentViewSet, \
    FeaturedArticleList

router = routers.DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'tag', TagViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'article', ArticleViewSet)
router.register(r'comment', CommentViewSet)

urlpatterns = [
    url(r'^featured/$', FeaturedArticleList.as_view()),
    url(r'^auth/signup/$', SignUpView.as_view(), name='signup'),
    url(r'^auth/login/$', LoginView.as_view(), name='api_token_auth'),
]
urlpatterns += router.urls
