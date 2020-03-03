from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from coreapp.models import Category, Tag, Article, Comment
from api.serializers import CategorySerializer, TagSerializer, ArticleSerializer, ArticleDetailSerializer, \
    CommentSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tag', 'category']

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleSerializer
        if self.action == 'retrieve':
            return ArticleDetailSerializer
        return ArticleDetailSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['article', 'user']
