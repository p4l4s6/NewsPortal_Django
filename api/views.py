from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets, generics, mixins
from coreapp.models import User, Category, Tag, Article, Comment
from api.serializers import UserSerializer, CategorySerializer, TagSerializer, ArticleListSerializer, \
    ArticleDetailSerializer, \
    ListCommentSerializer, CreateCommentSerializer


class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny, ]


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, ]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Article.objects.all().order_by('-updated_at')
    serializer_class = ArticleListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tag', 'category']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ArticleDetailSerializer
        else:
            return ArticleListSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CreateCommentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['article', 'user']

    def get_serializer_class(self):
        if self.action == 'list':
            return ListCommentSerializer
        if self.action == 'retrieve':
            return ListCommentSerializer
        return CreateCommentSerializer
