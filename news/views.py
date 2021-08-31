from django_filters import rest_framework as filters
from rest_framework import filters as rest_filters
from rest_framework import viewsets, mixins
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Article, ArticleComment
from .permissions import IsAuthorOrIsAdmin
from .serializers import ArticleSerializer, ArticleDetailsSerializer, CreateArticleSerializer, ArticleCommentSerializer


def index(self):
    return HttpResponse('Вы на главной странице!')


class ArticleFilter(filters.FilterSet):
    publish_at = filters.DateFromToRangeFilter('created_at', 'gte')

    class Meta:
        model = Article
        fields = ('publish_at',)


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()

    filter_backends = [filters.DjangoFilterBackend, rest_filters.SearchFilter,
                       rest_filters.OrderingFilter]
    filterset_class = ArticleFilter

    search_fields = ['title', 'category']
    ordering_fields = ['title', 'created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleSerializer
        elif self.action == 'retrieve':
            return ArticleDetailsSerializer
        return CreateArticleSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthorOrIsAdmin()]
        return []


class ArticleCommentViewSet(mixins.CreateModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):
    queryset = ArticleComment.objects.all()
    serializer_class = ArticleCommentSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAuthorOrIsAdmin()]
        return []

    @action(['GET'], detail=True)
    def comments(self, request, pk=None):
        article = self.get_object()
        comments = article.reviews.all()
        serializer = ArticleCommentSerializer(comments, many=True)
        return Response(serializer.data, status=200)

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
