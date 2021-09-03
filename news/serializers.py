from rest_framework import serializers

from .models import Article, ArticleComment, Like


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'author', 'created_at')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['likes'] = instance.likes.filter(like=True).count()
        return representation


class ArticleDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('title', 'content', 'image', 'author', 'category', 'comments', 'likes')


class CreateArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


class ArticleCommentSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ArticleComment
        fields = ('article', 'text', 'author', 'created_at', 'rating')

    def validate_product(self, article):
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


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ('article', 'like', 'in_bookmarks', 'rate')
