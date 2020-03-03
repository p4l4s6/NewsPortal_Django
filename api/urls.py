from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from api.views import SignUpView, UserViewSet, TagViewSet, CategoryViewSet, ArticleViewSet, CommentViewSet

router = routers.DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'tag', TagViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'article', ArticleViewSet)
router.register(r'comment', CommentViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/signup/$', SignUpView.as_view(), name='signup'),
    url(r'^auth/login/$', obtain_auth_token, name='api_token_auth'),
]
