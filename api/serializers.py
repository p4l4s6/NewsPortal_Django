from rest_framework import serializers
from coreapp.models import Category, Tag, Article


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    details = serializers.CharField(source='summary')

    class Meta:
        model = Article
        fields = ['title', 'details', 'thumbnail', 'updated_at']


class ArticleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
