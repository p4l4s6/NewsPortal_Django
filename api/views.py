from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework import viewsets, generics, mixins
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from api.serializers import UserSerializer, CategorySerializer, TagSerializer, ArticleListSerializer, \
    ArticleDetailSerializer, ListCommentSerializer, CreateCommentSerializer, FeaturedArticleSerializer
from coreapp.models import User, Category, Tag, Article, Comment, Featured


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'code': status.HTTP_200_OK,
                'message': 'Successfully logged in',
                'token': token.key,
                'id': user.pk,
                'email': user.email,
            })
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'message': 'Incorrect email or password',
            'details': serializer.errors
        })


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


class FeaturedArticleList(generics.ListAPIView):
    serializer_class = FeaturedArticleSerializer
    queryset = Featured.objects.filter(is_active=True).order_by('-updated_at')
