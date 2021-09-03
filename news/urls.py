from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ArticleViewSet, index, ArticleCommentViewSet, LikeView

router = DefaultRouter()

router.register('articles', ArticleViewSet)
router.register('comments', ArticleCommentViewSet)
router.register('likes', LikeView)

urlpatterns = [
    path('', index),
    path('', include(router.urls)),

]
