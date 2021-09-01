from django.db import models
from account.models import User


NEWS_CATEGORIES = (
    ('sport', 'Спорт'),
    ('science_and_tech', 'Наука и технологии'),
    ('culture', 'Культура'),
    ('politics', 'Политика'),
    ('economy', 'Экономика'),
    ('other', 'Разное'),
    ('world', 'Мир'),
)


class Article(models.Model):
    title = models.CharField(max_length=150)
    category = models.CharField(max_length=60, choices=NEWS_CATEGORIES, default='Разное')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='Articles', null=True, blank=True)
    author = models.ForeignKey(User, related_name='all', on_delete=models.CASCADE)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['title', 'category']

    def __str__(self):
        return self.title


class ArticleComment(models.Model):
    article = models.ForeignKey(Article,
                                on_delete=models.CASCADE,
                                related_name='comments')

    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comments')

    text = models.TextField()
    rating = models.SmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    #
    # def __str__(self):
    #     return self.article
