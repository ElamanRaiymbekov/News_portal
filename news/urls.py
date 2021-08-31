from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ArticleViewSet, index

router = DefaultRouter()

router.register('', ArticleViewSet)

urlpatterns = [
    path('', index),
    path('articles/', include(router.urls)),

]
