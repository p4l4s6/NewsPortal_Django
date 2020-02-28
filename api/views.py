from rest_framework import viewsets
from coreapp.models import Category, Tag, Article
from api.serializers import CategorySerializer, TagSerializer, ArticleSerializer, ArticleDetailSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleSerializer
        if self.action == 'retrieve':
            return ArticleDetailSerializer
        return ArticleDetailSerializer