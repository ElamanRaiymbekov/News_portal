from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Article, ArticleComment, Like

admin.site.register(Article)
admin.site.register(ArticleComment)


@admin.register(Like)
class LikeAdmin(ModelAdmin):
    pass
