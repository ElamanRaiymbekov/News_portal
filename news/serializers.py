import requests
from rest_framework import serializers

from .models import Article, ArticleComment, Like


class ArticleCommentSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ArticleComment
        fields = ('id', 'article', 'author', 'text', 'created_at', 'rating')

    def validate_comment(self, article):
        request = self.context.get('request')
        user = request.user
        if self.Meta.model.objects.filter(article=article, author=user).exists():
            raise serializers.ValidationError('Вы уже комментировали данную статью.')
        return article

    def validate_rating(self, rating):
        if rating not in range(1, 11):
            raise serializers.ValidationError('Рейтинг может быть от 1 до 10')
        return rating

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['author'] = request.user
        return super().create(validated_data)

class ArticleSerializer(serializers.ModelSerializer):
    comments = ArticleCommentSerializer(many=True)

    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'author', 'created_at', 'comments')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['likes'] = instance.likes.filter(like=True).count()
        return representation


class CreateArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


class ArticleDetailsSerializer(serializers.ModelSerializer):
    comments = ArticleCommentSerializer(many=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['likes'] = instance.likes.filter(like=True).count()
        return representation

    class Meta:
        model = Article
        fields = ('title', 'content', 'image', 'author', 'category', 'likes', 'comments')


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('user', 'article', 'like', 'in_bookmarks', 'rate')
