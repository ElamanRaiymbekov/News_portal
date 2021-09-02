from django_filters import rest_framework as filters
from rest_framework import filters as rest_filters
from rest_framework import viewsets, mixins
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from .models import Article, ArticleComment, Like
from news.permissions import IsAuthorOrIsAdmin
from .serializers import ArticleSerializer, ArticleDetailsSerializer, CreateArticleSerializer, ArticleCommentSerializer, \
    LikeSerializer


def index(self):
    return HttpResponse('Вы на главной странице!')


class ArticleFilter(filters.FilterSet):
    publish_at = filters.DateFromToRangeFilter('created_at', 'gte')

    class Meta:
        model = Article
        fields = ('id', 'author',)


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()

    filter_backends = [filters.DjangoFilterBackend, rest_filters.SearchFilter,
                       rest_filters.OrderingFilter]
    filterset_class = ArticleFilter

    search_fields = ['title', 'category', 'content']
    ordering_fields = ['id', 'title', 'created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleSerializer
        elif self.action == 'retrieve':
            return ArticleDetailsSerializer
        return CreateArticleSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return []


class ArticleCommentViewSet(viewsets.ModelViewSet):
    queryset = ArticleComment.objects.all()
    serializer_class = ArticleCommentSerializer

    class Meta:
        model = ArticleComment
        fields = ('author', 'text', 'created_at')

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAuthorOrIsAdmin()]
        return []

    @action(['GET'], detail=True)
    def comments(self, request, pk=None):
        article = self.get_object()
        comments = article.comments.all()
        serializer = ArticleCommentSerializer(comments, many=True)
        return Response(serializer.data, status=200)


class LikeView(mixins.UpdateModelMixin, GenericViewSet):

    permission_classes = [IsAuthenticated]
    queryset = Like.objects.all().count()
    print(queryset)
    serializer_class = LikeSerializer
    lookup_field = 'article'


    # def like(self, request, pk):
    #     article = self.get.objects()
    #     user = request.user
    #     like_obj, created = Like.objects.get_or_create(article=article, user=user)
    #
    #     if like_obj.is_liked:
    #         like_obj.is_liked = False
    #         like_obj.save()
    #         return Response('disliked')
    #     else:
    #         like_obj.is_liked = True
    #         like_obj.save()
    #         return Response('liked')





    # def get(self, request):
    #     articles = Article.objects.all()
    #     serializer = ArticleSerializer(articles, many=True)
    #     return Response({'articles': serializer.data})
    #
    # def post(self, request):
    #     article = request.data.get('article')
    #     serializer = ArticleSerializer(data=article)
    #
    #     if serializer.is_valid(raise_exception=True):
    #         article_saved = serializer.save()
    #     return Response({'succes': f'Article {article_saved.title} created successfully'})
    #
    # def put(self, request, pk):
    #     saved_article = get_object_or_404(Article.objects.all(), pk=pk)
    #     data = request.data.get('article')
    #     serializer = ArticleSerializer(instance=saved_article, data=data, partial=True)
    #
    #     if serializer.is_valid(raise_exception=True):
    #         article_saved = serializer.save()
    #
    #     return Response({
    #         'success': f'Article {article_saved.title} updated successfully'
    #     })
    #
    # def delete(self, request, pk):
    #     article = get_object_or_404(Article.objects.all())
    #     article.delete()
    #     return Response({
    #         'message': f'Article with id {pk} has been deleted.'
    #     }, status=204)
