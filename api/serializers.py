from rest_framework import serializers
from coreapp.models import User, Category, Tag, Article, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        read_only_fields = ['last_login', 'profile_pic']
        exclude = ('groups', 'is_staff', 'is_active', 'is_superuser', 'user_permissions')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects._create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super(UserSerializer, self).update(instance, validated_data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'thumbnail', ]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', ]


class ArticleListSerializer(serializers.ModelSerializer):
    details = serializers.CharField(source='summary')

    class Meta:
        model = Article
        fields = ['id', 'title', 'details', 'thumbnail', 'updated_at']


class ArticleDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    tag = TagSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Article
        fields = '__all__'
        depth = 1


class CreateCommentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ['article', 'details', 'user']


class ListCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    article = serializers.ReadOnlyField(source='article.id')

    class Meta:
        model = Comment
        fields = ['id', 'details', 'article', 'user', 'created_at']
        read_only_fields = ('id', 'article')
        depth = 1
