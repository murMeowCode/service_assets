from django.db import models
from django.conf import settings

class NewsItem(models.Model):
    title = models.CharField(max_length=150)
    content = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(upload_to='news_images/', blank=True, null=True)
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    news_item = models.ForeignKey(NewsItem, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=100, verbose_name='Автор комментария')
    text = models.TextField(max_length=500, verbose_name='Текст комментария')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
    
    def __str__(self):
        return f'Комментарий от {self.author} к новости "{self.news_item.title}"'

