from django.conf.urls import url, include
from rest_framework import routers, serializers, viewsets
from api.views import TagViewSet, CategoryViewSet, ArticleViewSet

router = routers.DefaultRouter()
router.register(r'tag', TagViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'article', ArticleViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
